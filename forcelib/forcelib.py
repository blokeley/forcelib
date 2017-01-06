"""Utility functions for working with force data from Mecmsin tensometers."""

import argparse
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Export public functions
__all__ = ('read_csv', 'work', 'plot_fd', 'plot_v_time',
           '_parse_args')


MAX_HEADER_ROWS = 10
"""Maximum number of header rows to search for start of data."""


def _count_headers(csv_data):
    """Return the number of header rows in the CSV string data.

    Header rows are defined by not starting with an integer.

    Raises:
        ValueError: if no line starting with an integer is found.
    """
    for line_num, line in enumerate(csv_data.splitlines()):
        try:
            int(line[0])
            return line_num

        except IndexError:
            # There is no text
            continue

        except ValueError:
            # There is text, but it cannot be converted to an int
            continue

    # Raise a ValueError if no end to the headers was found
    raise ValueError('Line starting with integer not found')


def read_csv(csv_filename, exclude=None):
    """Read the CSV file and return a multi-index DataFrame.

    Args:
        csv_filename (str or file pointer): CSV file from Emperor.
        exclude (list[int]): List of test numbers to exclude.  1-indexed.

    Returns:
        pandas.DataFrame: Columns are 'displacement (mm)',
                                      'force (N)', and
                                      'event (boolean)'.
                          Index is (test_name, time (s))
    """
    if exclude is None:
        exclude = []

    # Count number of header lines, up to MAX_HEADER_ROWS
    with open(csv_filename) as f:
        head = ''.join(next(f) for line_num in range(MAX_HEADER_ROWS))

    n_headers = _count_headers(head)

    # Read all CSV data into one big numpy.ndarray
    all_data = pd.read_csv(csv_filename, skiprows=n_headers, header=None)

    # Create column names so that test IDs are not lost
    test_names = ['Test {}'.format(i) for i in
                  range(1, 1 + (all_data.shape[1] // 4)) if i not in exclude]

    # Remove unwanted tests
    excluded = _exclude(all_data.shape[1], exclude)
    included = all_data.drop(all_data.columns[list(excluded)], axis=1)

    # Convert to a usable DataFrame
    return _to_dataframe(included, test_names)


def _exclude(n_columns, tests_to_exclude=None):
    """Return a sequence of column numbers to exclude.

    The returned sequence lists all 4 columns of those in the
    tests_to_exclude argument.

    Args:
        n_columns (int): the number of columns in the dataset.
        tests_to_exclude (sequence[int]): tests to exclude.

    Returns:
        A sequence of column numbers to exclude.
    """
    excluded = set()

    if tests_to_exclude:
        for test_num in tests_to_exclude:
            for col_num in range(4):
                excluded.add(col_num + 4 * (test_num - 1))

    return excluded


def _to_dataframe(df, test_names=None):
    """Convert basic DataFrame to MultiIndex DataFrame.

    Args:
        df [pandas.DataFrame]: raw DataFrame from CSV.
        test_names [list(str)]: list of test names.

    Returns:
        pandas.DataFrame: Columns are 'displacement', 'force' and 'event'.
            Index is (test_name, time)
    """
    n_cols = df.shape[1] // 4

    frames = []

    for test in range(n_cols):
        force_col = 4 * test
        frame = df.iloc[:, force_col:force_col + 4]
        frame.columns = ['force', 'displacement', 'time', 'event']

        # Convert minutes to seconds
        frame['time'] = frame['time'] * 60

        # Reindex on time
        frame.set_index('time', inplace=True)
        frames.append(frame)

    if not test_names:
        # Create test names
        test_names = ['Test {}'.format(i) for i in range(1, 1 + n_cols)]

    df_all = pd.concat(frames, keys=test_names)
    df_all.index.names = ('test', 'time')

    # Drop rows with NaNs
    df_all.dropna(inplace=True)

    # Convert events to booleans
    df_all['event'] = df_all['event'].astype(bool)

    return df_all


def work(df):
    """Calculate the work done in Joules.

    Work done is the area under the force-displacement curve.

    Args:
        df (pandas.DataFrame): DataFrame of force-displacement results.

    Returns:
        pandas.Series: Work done in Joules, with index of test names.
    """
    def _work(df):
        return np.trapz(df['force'], df['displacement']) / 1000

    return df.groupby(level='test').apply(_work)


def plot_fd(df, title=None, ax=None):
    """Plot force versus displacement on new figure, or on axes if given.

    Args:
        df (pandas.DataFrame): DataFrame to plot.
        title (str): Title of plot. Default: None.
        ax (matplotlib.axes.Axes): Axes to use. Default: Create new axes.

    Returns:
        matplotlib.axes.Axes: axes of plot.
    """
    if ax is None:
        fig, ax = plt.subplots()

    for name, group in df.groupby(level='test'):
        ax.plot(group['displacement'], group['force'], label=name)

    ax.legend(loc='best')
    ax.set_xlabel('Displacement (mm)')
    ax.set_ylabel('Force (N)')

    if title is not None:
        ax.set_title(title)

    return ax


def plot_v_time(df, title=None, events=False):
    """Plot force and  displacement versus time on new figure, or on axes
    if given.

    Why not just use `df.groupby(level='test').plot(subplots=True)`?  Because:

    1. The x labels are given as tuples like (Test 2, 0.00833) which is
       difficult to read.
    2. There is one figure for each test, which is unmanageable for large
       numbers of tests.

    Args:
        df (pandas.DataFrame): DataFrame to plot.
        title (str): Title of plot. Default: None.
        events (bool): Whether or not to plot events Default: False.

    Returns:
        list(matplotlib.axes.Axes): List of axes.
    """
    n_plots = 3 if events else 2
    fig, ax_arr = plt.subplots(n_plots, sharex=True)

    for name, group in df.groupby(level='test'):
        ax_arr[0].plot(df.loc[name].index, group['force'], label=name)
        ax_arr[1].plot(df.loc[name].index, group['displacement'], label=name)

        if events:
            ax_arr[2].plot(df.loc[name].index, group['event'], label=name)

    if title is not None:
        ax_arr[0].set_title(title)

    ax_arr[0].set_ylabel('Force N)')
    ax_arr[1].set_ylabel('Displacement (mm)')
    ax_arr[1].legend(loc='best')

    if events:
        ax_arr[2].set_ylabel('Event')
        ax_arr[2].set_xlabel('Time (s)')

    else:
        ax_arr[1].set_xlabel('Time(s)')

    return ax_arr


def _int_set(arg):
    """Convert comma-separated string to set of ints."""
    return set(int(n) for n in arg.split(','))


def _parse_args(description=None, args=None):
    """Convenience function to parse command line arguments.

    This function may be removed in future versions of forcelib.

    Args:
        description (str): Description of the program.
        args (list[str]): Command line arguments to parse.  Defaults to reading
                          from sys.argv.

    Returns:
        argparse.Namespace: Namespace object containing arguments.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', type=pathlib.Path, help='CSV file')

    msg = 'Comma-separated list of tests to exclude'
    parser.add_argument('-x', '--exclude', type=_int_set, help=msg)

    namespace = parser.parse_args(args)
    return namespace

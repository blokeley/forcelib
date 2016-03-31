"""Utility functions for working with force data from Mecmsin tensometers."""

import argparse
import logging
import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Export public functions
__all__ = ('read_csv', 'work', 'plot_force_v_displacement', '_parse_args')


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
            # print('{}: {}'.format(line_num, line))
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
    """Read the CSV file and return a list of `pandas.Series`.

    The index is the displacement in mm. The columns are the forces in N.
    """
    if exclude is None:
        exclude = []

    # Count number of header lines, up to 10 lines
    with open(csv_filename) as f:
        head = ''.join(next(f) for line_num in range(MAX_HEADER_ROWS))

    n_headers = _count_headers(head)

    # Read all CSV data into one big numpy.ndarray
    all_data = np.genfromtxt(csv_filename, delimiter=',',
                             skip_header=n_headers)

    # Create column names so that test IDs are not lost
    test_names = ['Test {}'.format(i) for i in
                  range(1, 1 + (all_data.shape[1] // 4)) if i not in exclude]

    # Remove unwanted tests
    excluded = _exclude(all_data.shape[1], exclude)
    forces = np.delete(all_data, list(excluded), axis=1)

    # Convert ndarray to DataFrame
    return _to_dataframe(forces, test_names)


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


def _to_dataframe(ndarray, test_names=None):
    """Convert numpy.ndarray to multi-index `pandas.DataFrame`.

    Args:
        ndarray [numpy.ndarray]: array to take data from.
        test_names [list(str)]: list of test names.

    Returns:
        pandas.DataFrame: Columns are 'displacement', 'force' and 'event'.
            Index is (test_name, time)
    """
    if not test_names:
        # Create test names
        test_names = ['Test {}'.format(i) for i in
                      range(1, 1 + (ndarray.shape[1] // 4))]

    frames = []

    for test in range(ndarray.shape[1] // 4):
        frame = pd.DataFrame({'force':  ndarray[:, 4 * test],
                              'displacement': ndarray[:, (4 * test) + 1],
                              'event': ndarray[:, (4 * test) + 3]},  # Event
                             index=ndarray[:, (4 * test) + 2])  # Time
        frames.append(frame)

    df_all = pd.concat(frames, keys=test_names)
    df_all.index.names = ('test', 'time')

    # Remove rows containing NaNs (which were shorter columns in the original
    # CSV file)
    df_all.dropna(inplace=True)

    # Convert events to integers
    df_all['event'] = df_all['event'].astype(bool)

    return df_all


def work(df, xmin=None, xmax=None):
    """Calculate the work done in Joules.

    Work done is the area under the force-displacement curve.

    Args:
        df (pandas.DataFrame): DataFrame of force-displacement results.
        xmin (float): minimum displacement (inclusive).
        xmax (float): maximum displacement (inclusive).
    """
    xmin = xmin if xmin is not None else df['displacement'].min()
    xmax = xmax if xmax is not None else df['displacement'].max()

    # slice(None) means select all from index 0.
    # slice(xmin, xmax) selects from index 1.
    # The ', :' at the end means select all columns
    view = df.loc[(slice(None), slice(xmin, xmax)), :]

    works = pd.Series(name='work')

    for name, group in view.groupby(level=0):
        works[name] = np.trapz(group['force'], group['displacement']) / 1000

    return works


def plot_force_v_displacement(df, title=None, ax=None):
    """Plot series on new figure, or on axes if given.

    Args:
        df (pandas.DataFrame): DataFrame to plot.
        title (str): Title of plot.
        ax (matplotlib.axes.Axes): Axes to use.

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


def _int_set(arg):
    """Convert comma-separated string to set of ints."""
    return set(int(n) for n in arg.split(','))


def _parse_args(description=None, args=None):
    """Convenience function to parse command line arguments.

    This function may be removed in future versions of forcelib.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', type=pathlib.Path, help='CSV file')

    msg = 'Comma-separated list of tests to exclude'
    parser.add_argument('-x', '--exclude', type=_int_set, help=msg)

    namespace = parser.parse_args(args)
    logging.debug(namespace)
    return namespace

# MIT License
#
# Copyright (c) 2017 Tom Oakley
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Get the latest version from https://github.com/blokeley/forcelib

"""Utility functions for working with force data from Mecmsin tensometers."""

import argparse
import pathlib
from typing import Callable, Iterable, List, Optional, Set, Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


__version__ = '1.5.1'

# Export public functions
__all__ = ('read_csv', 'work', 'plot', 'bar', 'set_names', '_parse_args')

_HEADER_ROWS_MAX = 10
"""Maximum number of header rows to search in CSV for start of data."""

_COLS_PER_TEST = 4
"""Columns of data in CSV file for each test."""


def _count_headers(csv_data: str) -> int:
    """Return the number of header rows in the CSV string data.

    Header rows are defined by having a number in their second column because
    the first column contains the sample (test) name which could be a number.

    Raises:
        ValueError: if cell is empty or cannot be converted to a float.
    """
    for line_num, line in enumerate(csv_data.splitlines()):
        try:
            # Try converting the second column to a float
            float(line.split(',')[1])
            return line_num

        except ValueError:
            # Empty cell, or cannot be converted to a float
            continue

    # Raise a ValueError if no end to the headers was found
    raise ValueError('Line starting with integer not found')


def _get_test_names(csv_data: str) -> Iterable[str]:
    """Return a list of test names"""
    test_name_row = csv_data.splitlines()[2]
    return test_name_row.split(',')[::_COLS_PER_TEST]


def read_csv(csv_filename: str, exclude: Set[int]=None) -> pd.DataFrame:
    """Read the CSV file and return a multi-index DataFrame.

    Args:
        csv_filename (str or file pointer): CSV file from Emperor.
        exclude: Set of test numbers to exclude.  1-indexed.

    Returns:
        DataFrame with columns of ('displacement (mm)', 'force (N)',
        'minutes', 'event (boolean)').
        The index is a MultiIndex of (test_name, time (s))
    """
    # Count number of header lines, up to _HEADER_ROWS_MAX
    with open(csv_filename) as f:
        head = ''.join(next(f) for line_num in range(_HEADER_ROWS_MAX))

    n_headers = _count_headers(head)
    test_names = _get_test_names(head)

    # Read all CSV data into one big pd.DataFrame
    all_data = pd.read_csv(csv_filename, skiprows=n_headers, header=None)

    # Remove unwanted tests
    excluded = _exclude(exclude)
    included = all_data.drop(all_data.columns[list(excluded)], axis=1,
                             errors='ignore')

    # Convert to a usable DataFrame
    return _to_dataframe(included, test_names)


def _exclude(tests_to_exclude: Optional[Set[int]]) -> Set[int]:
    """Return a sequence of column numbers to exclude.

    The returned sequence lists all columns of those in the
    tests_to_exclude argument.
    """
    excluded = set()

    if tests_to_exclude:
        for test_num in tests_to_exclude:
            for col_num in range(_COLS_PER_TEST):
                excluded.add(col_num + _COLS_PER_TEST * (test_num - 1))

    return excluded


def _to_dataframe(df: pd.DataFrame, test_names: Iterable[str]=None) \
                  -> pd.DataFrame:
    """Convert basic DataFrame to MultiIndex DataFrame.

    Args:
        df: raw pandas.DataFrame from CSV.
        test_names: list of test names.

    Returns:
        DataFrame with columns ('displacement (mm)', 'force (N)',
        'minutes', 'event (boolean)'). Index is (test_name, time)
    """
    n_cols = df.shape[1] // _COLS_PER_TEST

    frames = []

    for force_col in range(0, n_cols * _COLS_PER_TEST, _COLS_PER_TEST):
        frame = df.iloc[:, force_col:force_col + _COLS_PER_TEST].copy()
        frame.columns = ['force', 'displacement', 'minutes', 'event']
        frame.dropna(inplace=True)

        # Set the index to time in seconds
        frame.set_index(frame['minutes'] * 60, inplace=True)
        frames.append(frame)

    df_all = pd.concat(frames, keys=test_names)
    df_all.index.names = ('test', 'time')

    # Convert events to booleans
    df_all['event'] = df_all['event'].astype(bool)

    return df_all


def set_names(df: pd.DataFrame, names: Iterable[str]) -> None:
    """Set the test names.

    Args:
        df: A pandas.DataFrame with a MultiIndex of (test_name, time)
        names: A sequence of test names to use
    """
    df.index.set_levels(names, level=0, inplace=True)


def work(df: pd.DataFrame) -> pd.Series:
    """Calculate the work done in Joules.

    Work done is the area under the force-displacement curve.

    Args:
        df: Force-displacement results.

    Returns:
        Work done in Joules, with index of test names.
    """
    def _work(df):
        return np.trapz(df['force'], df['displacement']) / 1000

    return df.groupby(level=0).apply(_work)


def plot(df: pd.DataFrame, x: str='displacement', y: List[str]=['force'],
         title: str=None, ax: mpl.axes.Axes=None) -> Iterable[plt.Axes]:
    """Plot given columns (y) on new figure, or on axes ax if given.

    Why not just use `df.groupby(level='test').plot(subplots=True)`?  Because:

    1. The x labels are given as tuples like (Test 2, 0.00833) which is
       difficult to read.
    2. There is one figure for each test, which is unmanageable for large
       numbers of tests.

    Args:
        df: DataFrame to plot.
        x: Name of column to use as x axis.
        y: Names of columns to plot on y axes.
        title: Title of plot. Default: None.

    Returns:
        List of axes.
    """
    num_plots = len(y)

    if ax:
        axes = ax
        fig = ax.get_figure()

    else:
        fig, axes = plt.subplots(num_plots, sharex=True)

    for name, group in df.groupby(level=0):
        # Remove the test name level from the index
        group.reset_index(inplace=True)

        try:
            # Assume axes is an array of axes
            for ax_num, ax in enumerate(axes):
                ax.plot(group[x], group[y[ax_num]], label=name)
                ax.set_ylabel(y[ax_num])

        except TypeError:
            # Only 1 axis
            axes.plot(group[x], group[y[0]], label=name)
            axes.set_ylabel(y[0])

    try:
        # Assume axes is an array of axes
        if title is not None:
            axes[0].set_title(title)

        axes[num_plots - 1].legend(loc='best')
        axes[num_plots - 1].set_xlabel(x)

    except TypeError:
        # Only 1 axis
        if title is not None:
            axes.set_title(title)

        axes.legend(loc='best')
        axes.set_xlabel(x)

    # Reize for multiple subplots
    width, height = fig.get_size_inches()
    fig.set_size_inches(width, num_plots * height)
    plt.tight_layout()

    return axes


def bar(df: pd.DataFrame,
        title: str='Mean force (N). Each error bar is 1 standard deviation',
        y: str='force', agg: Callable[[None], np.ndarray]=np.mean,
        yerr: Callable[[None], np.ndarray]=np.std) -> plt.Axes:
    """Return bar chart of aggregate function 'agg' applied to column y.

    Error bars can be set by an aggregate function yerr.

    Args:
        df: The DataFrame to act on.
        title: The chart title.
        agg (function): Function to apply.  For examples, see
        https://docs.scipy.org/doc/numpy-1.10.1/reference/routines.math.html
        yerr (function): Aggregate function to calculate error bars.
                         Set to None for no error bars.
    """
    group = df.groupby(level=0)[y]

    # Plot aggregate as a bar chart, with error bars
    ax = group.agg(agg).plot(kind='bar', title=title, yerr=group.agg(yerr))
    ax.set_ylabel(y)

    if title:
        ax.set_title(title)

    return ax


def _int_set(arg: str) -> Set[int]:
    """Convert comma-separated string to set of ints."""
    return set(int(n) for n in arg.split(','))


def _parse_args(description: str=None, args: Optional[Sequence[str]]=None) \
                -> argparse.Namespace:
    """Convenience function to parse command line arguments.

    This function may be removed in future versions of forcelib.

    Args:
        description: Description of the program.
        args: Command line arguments to parse.  Defaults to sys.argv.

    Returns:
        Namespace object containing arguments.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('file', type=pathlib.Path, help='CSV file')

    msg = 'Comma-separated list of tests to exclude'
    parser.add_argument('-x', '--exclude', type=_int_set, help=msg)

    namespace = parser.parse_args(args)
    return namespace

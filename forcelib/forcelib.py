"""Utility functions for working with force data from Mecmsin tensometers."""

import argparse
import logging
import pathlib

import numpy as np
import pandas as pd


# Export public functions
__all__ = ('read_forces', 'work')
__version__ = '0.1.0'


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


def read_forces(csv_filename, exclude=None):
    """Read the CSV file and return a `pandas.DataFrame`.

    The index is the distance in mm. The columns are the forces in N.
    """
    # Count number of header lines, up to 10 lines
    with open(csv_filename) as f:
        head = ''.join(next(f) for line_num in range(MAX_HEADER_ROWS))

    n_headers = _count_headers(head)

    # Read all CSV data into one big numpy.ndarray
    all_data = np.genfromtxt(csv_filename, delimiter=',',
                             skip_header=n_headers)

    # Create column names so that sample IDs are not lost
    columns = ['Sample {}'.format(i) for i in
               range(1, 1 + (all_data.shape[1] / 4)) if i not in exclude]

    # Remove unwanted columns and unwanted samples (tests)
    excluded = _exclude(all_data.shape[1], exclude)
    forces = np.delete(all_data, list(excluded), axis=1)

    # Convert ndarray to DataFrame
    return _ndarray_to_dataframe(forces, columns)


def _exclude(n_samples, samples_to_exclude=None):
    """Return a sequence of column numbers to exclude.

    The returned sequence lists:
        1. The time column (column 2 of the 0,1,2,3 for each sample).
        1. The event column (column 3 of the 0,1,2,3 for each sample),
        2. All 4 columns of those in the samples_to_exclude argument.

    Args:
        n_samples (int): the number of samples in the dataset.
        samples_to_exclude (sequence[int]): samples to exclude.

    Returns:
        A sequence of column numbers to exclude.
    """
    excluded = set()

    # Remove event column (every fourth column, starting at 3)
    for col_num in range(2, n_samples, 4):
        excluded.add(col_num)  # Time column
        excluded.add(col_num + 1)  # Event column

    # Remove samples_to_exclude
    if samples_to_exclude:
        for sample_num in samples_to_exclude:
            for col_num in range(4):
                excluded.add(col_num + 4 * (sample_num - 1))

    return excluded


def _to_list_of_series(ndarray, sample_names):
    """Convert numpy.ndarray to list of `pandas.Series`.

    Args:
        ndarray [numpy.ndarray]: array to take data from.
        sample_names [list(str)]: list of sample names.

    Returns:
        list(pandas.Series): list of Series of force-distance results.
    """
    list_of_series = []

    for sample in range(0, ndarray.shape[1] // 2, 2):
        series = pd.Series(ndarray[:, sample], ndarray[:, sample + 1],
                           name=[sample_names[sample]])
        series.index.name = 'Distance (mm)'
        list_of_series.append(series)

    return list_of_series


def index_distance(dataframe):
    """Transform the DataFrame to have distances as the index.

    The dataframe should be in the CSV format exported by Mecmesin Emperor
    software. Namely, colums of [force, distance, time, event]. time and
    event are unused.

    """
    raise NotImplemented


def work(dataframe, column, xmin=-np.inf, xmax=np.inf):
    """Calculate the work done in Joules.

    Work done is the area under the force-displacement curve.

    Args:
    dataframe (DataFrame): dataframe to work on
    column (str): column name
    xmin (float): minimum displacement (inclusive)
    xmax (float): maximum displacement (exclusive)
    """
    raise NotImplementedError('Needs unit tests')

    return np.trapz(view[column], view.index)


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

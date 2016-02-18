"""Utility functions for working with force data from Mecmsin tensometers."""

import argparse
import logging
import pathlib

import numpy as np


# Export public functions
__all__ = ('read_csv', 'work')
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


def read_csv(csv_filename, exclude=None):
    """Read the CSV file and return a `pandas.DataFrame`.

    The index is the distance in mm. The columns are the forces in N.
    """
    # Count number of header lines, up to 10 lines
    with open(csv_filename) as f:
        head = ''.join(next(f) for line_num in range(MAX_HEADER_ROWS))

    n_headers = _count_headers(head)

    arrays = np.genfromtxt(csv_filename, delimiter=',', skip_header=n_headers)

    # Remove unwanted columns
    np.delete(arrays, list(excluded), axis=0)

    # TODO: Convert ndarray to DataFrame
    return arrays


def _exclude(arr, samples_to_exclude):
    """TODO: update docstring
    Return a sequence of column numbers to exclude.

    Create a sequence with  the event column (column 3 of the 4 for each sample),
    and all 4 columns of those in the samples_to_exclude argument.

    Args:
        samples_to_exclude (sequence[int]): samples to exclude
    """
    excluded = set()

    if samples_to_exclude:
        for test_num in samples_to_exclude:
            for col_num in range(3):
                excluded.add(col_num + test_num for col_num in range(3))

    # Remove event column (every third column)
    for col_num in range(3, arr.shape[1], 3):
        excluded.add(col_num)


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
    view = dataframe[(dataframe.index >= xmin) & (dataframe.index < xmax)]
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

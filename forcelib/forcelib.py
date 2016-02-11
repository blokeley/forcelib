"""Utility functions for working with force data from Mecmsin tensometers."""

import argparse
import logging
import pathlib

import numpy as np


# Export public functions
__all__ = ('read_csv', 'work')


def read_csv(csv_filename, exclude=None):
    """Read the CSV file and return a `pandas.DataFrame`.

    The index is the distance in mm. The columns are the forces in N.
    """
    excluded = set()

    if exclude:
        for test_num in exclude:
            for col_num in range(3):
                excluded.add(col_num + test_num for col_num in range(3))

    arrays = np.genfromtxt(csv_filename, delimiter=',', skip_header=3)

    # Remove event column (every third column)
    for col_num in range(3, arrays.size[1], 3):
        excluded.add(col_num)

    # Remove unwanted columns
    np.delete(arrays, excluded, axis=0)

    # TODO: Convert ndarray to DataFrame


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

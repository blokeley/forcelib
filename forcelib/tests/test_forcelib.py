"""Unit tests for forcelib.py."""

import unittest

import numpy as np
import pandas as pd

from ..forcelib import (_parse_args, _count_headers, _int_set, _exclude,
                        _to_dataframe, work)


def assertFrameEqual(df1, df2, **kwds):
    """ Assert that two dataframes are equal, ignoring ordering of columns"""
    from pandas.util.testing import assert_frame_equal
    return assert_frame_equal(df1.sort_index(axis=1), df2.sort_index(axis=1),
                              check_names=True, **kwds)


class TestParseArgs(unittest.TestCase):

    def test_path(self):
        p = r'..\test.csv'
        args = _parse_args(args=[p])
        self.assertEqual(p, str(args.file))


class TestIntSet(unittest.TestCase):

    def test_int_set(self):
        expected = {1, 2, 3}
        self.assertEqual(expected, _int_set('1,2,3'))


class TestCountHeaders(unittest.TestCase):

    def test_count_headers(self):
        # Tests defined as expected number, input text
        tests = (
            (3, "A\nB\nC\n0\n"),
            (4, "A\nB\nC\nD\n0\n"),
            (4, "A\nB\n\nD\n0\n"))

        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(test[0], _count_headers(test[1]))

    def test_no_integer(self):
        with self.assertRaises(ValueError):
            _count_headers("A\nB\nC\n")


class TestArrayFunctions(unittest.TestCase):

    def setUp(self):
        # Set up table
        self.df = pd.DataFrame([[1.2, 0., 0.1, 0, 0.8, 0, 0.1, 1],
                                [1.3, 0.3, 0.2, 1, 0.5, 0, 0.25, 1],
                                [1.4, 0.2, 0.3, 0, 0.7, 0.3, 0.3, 1],
                                [1.5, 0.5, 0.4, 1, 0.8, 0.2, 0.4, 0],
                                [1.6, 0.5, 0.45, 0, np.nan, np.nan, np.nan,
                                np.nan]])

    def test_to_dataframe(self):
        test_names = ['Test {}'.format(i) for i in range(1, 3)]

        frames = [pd.DataFrame({'force': [1.2, 1.3, 1.4, 1.5, 1.6],
                                'displacement': [0.0, 0.3, 0.2, 0.5, 0.5],
                                'event': [False, True, False, True, False],
                                },
                               index=[6.0, 12, 18, 24, 27]),
                  pd.DataFrame({'force': [0.8, 0.5, 0.7, 0.8],
                                'displacement': [0.0, 0.0, 0.3, 0.2],
                                'event':[True, True, True, False]},
                               index=[6.0, 15, 18, 24])]

        expected = pd.concat(frames, keys=test_names)
        expected.index.names = ('test', 'time')

        # Create the results DataFrame
        result = _to_dataframe(self.df, test_names)

        # Run test
        assertFrameEqual(result, expected)

    def test_work(self):
        expected = pd.Series((0.675e-3, 0.105e-3),
                             index=('Test 1', 'Test 2'),
                             name='test')

        df = _to_dataframe(self.df)
        self.assertTrue(work(df).equals(expected))


class TestExclude(unittest.TestCase):

    def setUp(self):
        self.n_tests = 20

    def test_exclude(self):
        excluded = {1, 3}
        expected = {0, 1, 2, 3, 8, 9, 10, 11}
        self.assertEqual(expected, _exclude(self.n_tests, excluded))

    def test_none(self):
        # Assert no change if excluded is None or empty sequence
        self.assertEqual(set(), _exclude(self.n_tests, None))
        self.assertEqual(set(), _exclude(self.n_tests, set()))

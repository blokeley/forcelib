"""Unit tests for forcelib.py"""

import unittest
import pathlib
from pprint import pprint

import numpy as np
import pandas as pd

from ..forcelib import (_parse_args, _count_headers, _int_set, _exclude,
                        _ndarray_to_dataframe)


@unittest.skip
class TestParseArgs(unittest.TestCase):

    def test_path(self):
        p = r'..\test.csv'
        argv = [p]
        args = _parse_args(argv)
        self.assertEqual(p, str(args.path))

    def test_pathlib(self):
        p = r'..\test.csv'
        path = pathlib.Path(p)
        self.assertEqual(p, str(path))


class TestIntSet(unittest.TestCase):

    def test_int_set(self):
        expected = {1, 2, 3}
        self.assertEqual(expected, _int_set('1,2,3'))


class TestCountHeaders(unittest.TestCase):

    def test_count_headers(self):
        # Tests defined as expected number, input text
        tests = (
            (3, "A\nB\nC\n0\n"),
            (4, "A\nB\nC\nD\n0\n"))

        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(test[0], _count_headers(test[1]))

    def test_no_integer(self):
        with self.assertRaises(ValueError):
            _count_headers("A\nB\nC\n")


class TestNdarrayToDataframe(unittest.TestCase):

    def test_ndarray_to_dataframe(self):
        # Set up table
        arr = np.array([[1.2, 0.0, 0.5, 0.0],
                        [1.3, 0.1, 0.6, 0.0],
                        [1.4, 0.2, 0.7, 0.3],
                        [1.5, 0.5, 0.8, 0.6]])

        columns = ['Sample {}'.format(i) for i in range(1, 3)]

        # TODO: Create expected DataFrame
        # expected  = pd.DataFrame([{'Sample 1': }])
        # Run test
        df = _ndarray_to_dataframe(arr, columns)

        # self.assertEqual(expected, df)


class TestExclude(unittest.TestCase):

    def setUp(self):
        self.n_samples = 20

    def test_exclude(self):
        excluded = {1, 3}
        expected = {0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 14, 15, 18, 19}
        self.assertEqual(expected, _exclude(self.n_samples, excluded))

    def test_none(self):
        # Assert no change if excluded is None or empty sequence
        expected = {2, 3, 6, 7, 10, 11, 14, 15, 18, 19}
        self.assertEqual(expected, _exclude(self.n_samples, None))
        self.assertEqual(expected, _exclude(self.n_samples, set()))


@unittest.skip
class TestIndexDistance(unittest.TestCase):

    def setUp(self):
        self.data = []

        for row in range(10):
            for testnum in range(4):
                d = {'force{}'.format(testnum): row * testnum,
                     'distance{}'.format(testnum): 2.3 + row,
                     'time{}'.format(testnum): row + testnum,
                     'event{}'.format(testnum): 0}
                self.data.append(d)

        pprint(self.data)

        self.df = pd.DataFrame(self.data)
        print(self.df)

    def test_reindex(self):
        pass

if __name__ == '__main__':
    unittest.main()

"""Unit tests for forcelib.py"""

import unittest
import pathlib
from pprint import pprint

import pandas as pd

from .. import forcelib
# thing


@unittest.skip
class TestParseArgs(unittest.TestCase):

    def test_path(self):
        p = r'..\test.csv'
        argv = [p]
        args = forcelib.parse_args(argv)
        self.assertEqual(p, str(args.path))

    def test_pathlib(self):
        p = r'..\test.csv'
        path = pathlib.Path(p)
        self.assertEqual(p, str(path))


class TestIntSet(unittest.TestCase):

    def test_int_set(self):
        expected = set((1, 2, 3))
        self.assertEqual(expected, forcelib._int_set('1,2,3'))


class TestCountHeaders(unittest.TestCase):

    def test_count_headers(self):
        # Tests defined as expected number, input text
        tests = (
            (3, "A\nB\nC\n0\n"),
            (4, "A\nB\nC\nD\n0\n"))

        for test in tests:
            with self.subTest(test=test):
                self.assertEqual(test[0], forcelib._count_headers(test[1]))

    def test_no_integer(self):
        with self.assertRaises(ValueError):
            forcelib._count_headers("A\nB\nC\n")


class TestExclude(unittest.TestCase):

    def test_exclude(self):
        excluded = (1, 3, 4)
        # TODO: Create an example array for testing
        # arr =


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

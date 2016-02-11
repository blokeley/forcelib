"""Unit tests for forcelib.py"""

import unittest
import pathlib
from pprint import pprint

import pandas as pd

import forcelib


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

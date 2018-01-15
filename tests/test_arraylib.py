"""Unit tests for arraylib.py."""

import unittest

import numpy as np
import pandas as pd

from arraylib import rescale, interp
from tests.test_forcelib import assertFrameEqual


class TestRescale(unittest.TestCase):

    def test_rescale(self):
        # Create a dummy array x
        index_ = np.asarray((2, 2.5, 3, 6, 7, 12, 15, 18, 20, 27))
        x = np.sin(index_ / 10)
        min_ = -4
        max_ = 45
        scaled_x = rescale(x, min_, max_)

        self.assertEqual(scaled_x.shape, x.shape)
        self.assertEqual(scaled_x.min(),  min_)
        self.assertEqual(scaled_x.max(), max_)
        # Assert that the scaled array correlates perfectly
        # with the original array
        self.assertTrue(np.array_equal(
                        np.corrcoef(x, scaled_x),
                        np.array([[1., 1.], [1., 1.]])))


class TestInterp(unittest.TestCase):

    def test_interp(self):
        df = pd.DataFrame(dict(A=(1, 2, 3, 4), B=(10, 8, 6, 4)))
        new_length = 7
        new_index = np.linspace(1, 3, new_length)
        interped = interp(df, new_index)

        expected = pd.DataFrame(dict(A=np.linspace(2, 4, new_length),
                                     B=np.linspace(8, 4, new_length)),
                                index=new_index)
        assertFrameEqual(expected, interped)

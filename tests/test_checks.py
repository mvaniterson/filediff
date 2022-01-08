"""Unit tests for module checks"""
import unittest
import logging

import pandas as pd

from src.checks import (
    nrows_equal,
    ncols_equal,
    cols_equal,
    dtypes_equal,
    values_equal,
    compare_dataframes,
)

logger = logging.getLogger("compare_dataframes")
logger.setLevel(logging.ERROR)


class TestCompareDataFrames(unittest.TestCase):
    def setUp(self):
        self.a = pd.DataFrame(
            {"col_1": ["a", "b", "c"], "col_2": [1, 2, 3], "col_3": [1.1, 1.2, 1.3]}
        )
        self.c = pd.DataFrame(
            {"col_1": ["a", "b"], "col_2": [1, 2], "col_3": [1.1, 1.2]}
        )
        self.d = pd.DataFrame({"col_1": ["a", "b", "c"], "col_2": [1, 2, 3]})
        self.e = pd.DataFrame(
            {"col_2": [1, 2, 3], "col_1": ["a", "b", "c"], "col_3": [1.1, 1.2, 1.3]}
        )
        self.f = pd.DataFrame(
            {"col_0": ["a", "b", "c"], "col_2": [1, 2, 3], "col_3": [1.1, 1.2, 1.3]}
        )
        self.g = pd.DataFrame(
            {
                "col_1": ["a", "b", "c"],
                "col_2": [1.0, 2.0, 3.0],
                "col_3": [1.1, 1.2, 1.3],
            }
        )
        self.h = pd.DataFrame(
            {"col_2": [1, 2, 3], "col_3": [1.1, 1.2, 1.3], "col_1": ["a", "b", "d"]}
        )

    def test_nrows_equal(self):
        self.assertTrue(nrows_equal(self.a, self.a))

    def test_nrows_differ(self):
        self.assertFalse(nrows_equal(self.a, self.c))

    def test_ncols_equal(self):
        self.assertTrue(ncols_equal(self.a, self.a))

    def test_ncols_differ(self):
        self.assertFalse(ncols_equal(self.a, self.d))

    def test_cols_equal(self):
        self.assertTrue(cols_equal(self.a, self.a))

    def test_cols_order_differ(self):
        self.assertFalse(cols_equal(self.a, self.e))

    def test_cols_names_differ(self):
        self.assertFalse(cols_equal(self.a, self.f))

    def test_dtypes_equal(self):
        self.assertTrue(dtypes_equal(self.a, self.a))

    def test_dtypes_differ(self):
        self.assertFalse(dtypes_equal(self.a, self.g))

    def test_values_equal(self):
        self.assertTrue(values_equal(self.a, self.a, orderby="col_1"))

    def test_values_differ(self):
        self.assertFalse(values_equal(self.a, self.h, orderby="col_1"))

    def test_compare_dataframes_equal(self):
        self.assertTrue(compare_dataframes(self.a, self.a, orderby="col_1"))

    def test_compare_dataframes_differ1(self):
        self.assertFalse(compare_dataframes(self.a, self.g, orderby="col_1"))

    def test_compare_dataframes_differ2(self):
        self.assertFalse(compare_dataframes(self.a, self.h, orderby="col_1"))

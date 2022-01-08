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
        self.dataframe_a = pd.DataFrame(
            {"col_1": ["a", "b", "c"], "col_2": [1, 2, 3], "col_3": [1.1, 1.2, 1.3]}
        )
        self.dataframe_c = pd.DataFrame(
            {"col_1": ["a", "b"], "col_2": [1, 2], "col_3": [1.1, 1.2]}
        )
        self.dataframe_d = pd.DataFrame({"col_1": ["a", "b", "c"], "col_2": [1, 2, 3]})
        self.dataframe_e = pd.DataFrame(
            {"col_2": [1, 2, 3], "col_1": ["a", "b", "c"], "col_3": [1.1, 1.2, 1.3]}
        )
        self.dataframe_f = pd.DataFrame(
            {"col_0": ["a", "b", "c"], "col_2": [1, 2, 3], "col_3": [1.1, 1.2, 1.3]}
        )
        self.dataframe_g = pd.DataFrame(
            {
                "col_1": ["a", "b", "c"],
                "col_2": [1.0, 2.0, 3.0],
                "col_3": [1.1, 1.2, 1.3],
            }
        )
        self.dataframe_h = pd.DataFrame(
            {"col_2": [1, 2, 3], "col_3": [1.1, 1.2, 1.3], "col_1": ["a", "b", "d"]}
        )

    def test_nrows_equal(self):
        self.assertTrue(nrows_equal(self.dataframe_a, self.dataframe_a))

    def test_nrows_differ(self):
        self.assertFalse(nrows_equal(self.dataframe_a, self.dataframe_c))

    def test_ncols_equal(self):
        self.assertTrue(ncols_equal(self.dataframe_a, self.dataframe_a))

    def test_ncols_differ(self):
        self.assertFalse(ncols_equal(self.dataframe_a, self.dataframe_d))

    def test_cols_equal(self):
        self.assertTrue(cols_equal(self.dataframe_a, self.dataframe_a))

    def test_cols_order_differ(self):
        self.assertFalse(cols_equal(self.dataframe_a, self.dataframe_e))

    def test_cols_names_differ(self):
        self.assertFalse(cols_equal(self.dataframe_a, self.dataframe_f))

    def test_dtypes_equal(self):
        self.assertTrue(dtypes_equal(self.dataframe_a, self.dataframe_a))

    def test_dtypes_differ(self):
        self.assertFalse(dtypes_equal(self.dataframe_a, self.dataframe_g))

    def test_values_equal(self):
        self.assertTrue(
            values_equal(self.dataframe_a, self.dataframe_a, orderby="col_1")
        )

    def test_values_differ(self):
        self.assertFalse(
            values_equal(self.dataframe_a, self.dataframe_h, orderby="col_1")
        )

    def test_compare_dataframes_equal(self):
        self.assertTrue(
            compare_dataframes(self.dataframe_a, self.dataframe_a, orderby="col_1")
        )

    def test_compare_dataframes_differ1(self):
        self.assertFalse(
            compare_dataframes(self.dataframe_a, self.dataframe_g, orderby="col_1")
        )

    def test_compare_dataframes_differ2(self):
        self.assertFalse(
            compare_dataframes(self.dataframe_a, self.dataframe_h, orderby="col_1")
        )

"""Checks to compare two DataFrames"""
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def nrows_equal(dataframe_a, dataframe_b):
    """check if row numbers are equal between two DataFrames"""

    nrowsa, _ = dataframe_a.shape
    nrowsb, _ = dataframe_b.shape

    if nrowsa == nrowsb:
        logger.info("Number of rows are equal %s", nrowsa)
        return True
    logger.warning("Number of rows differ %s vs %s", nrowsa, nrowsb)
    return False


def ncols_equal(dataframe_a, dataframe_b):
    """check if column numbers are equal between two DataFrames"""

    _, ncolsa = dataframe_a.shape
    _, ncolsb = dataframe_b.shape

    if ncolsa == ncolsb:
        logger.info("Number of columns are equal %s", ncolsa)
        return True
    logger.warning("Number of columns differ %s vs %s", ncolsa, ncolsb)
    return False


def cols_equal(dataframe_a, dataframe_b):
    """check if column names are equal between two DataFrames"""

    columnsa = dataframe_a.columns
    columnsb = dataframe_b.columns

    if np.array_equal(columnsa, columnsb):
        logger.info("Column names are equal")
        return True
    if set(columnsa) == set(columnsb):
        logger.warning("Column names are equal but their order is different")
        return False
    logger.warning("Column names differ")
    return False


def dtypes_equal(dataframe_a, dataframe_b):
    """check if column dtypes are equal between two DataFrames"""

    dtypesa = dataframe_a.dtypes
    dtypesb = dataframe_b.dtypes

    if np.array_equal(dtypesa, dtypesb):
        logger.info("dtypes of columns are equal")
        return True
    logger.warning("dtypes of columns differ")
    return False

def get_differences(dataframe_a, dataframe_b):
    """Show the differences between two DataFrames"""

    dataframe_a.columns = [col + '_file1' for col in dataframe_a.columns]
    dataframe_b.columns = [col + '_file2' for col in dataframe_b.columns]

    dataframe_c = pd.concat([dataframe_a.reset_index(drop=True), dataframe_b], axis=1)

    dataframe_c['differences'] = False
    for col in dataframe_a.columns:
        dataframe = dataframe_c[[col, col.replace('_file1', '_file2')]]
        dataframe_c['differences'] += dataframe.iloc[:, 0] != dataframe.iloc[:, 1]

    return dataframe_c[dataframe_c['differences']]


def values_equal(dataframe_a, dataframe_b, orderby=None):
    """check if values are equal between two DataFrames"""

    if orderby:
        dataframe_a = dataframe_a.sort_values(by=orderby).reset_index(drop=True)
        dataframe_b = dataframe_b.sort_values(by=orderby).reset_index(drop=True)

    columns = []
    for col in dataframe_a.columns:
        if dataframe_a[col].dtype == np.float64:
            equal = np.allclose(
                dataframe_a[col],
                dataframe_b[col],
                rtol=1e-05,
                atol=1e-08,
                equal_nan=False,
            )
        else:
            equal = np.array_equal(
                dataframe_a[col].values, dataframe_b[col].values, equal_nan=False
            )
        columns.append(equal)

    if all(columns):
        logger.info("For every column all values are equal (up to row ordering)")
        return True
    logger.info(
        "Columns %s have differing values", ", ".join(dataframe_a.columns[columns])
    )

    dataframe_c = get_differences(dataframe_a, dataframe_b)

    logging.info('There are %s differences', str(dataframe_c['differences'].sum()))
    logger.info('Differences head - %s',  dataframe_c.head())

    return False


def compare_dataframes(dataframe_a, dataframe_b, orderby):
    """Run all tests on two DataFrames"""

    tests = [nrows_equal, ncols_equal, cols_equal, dtypes_equal]
    for test in tests:
        if not test(dataframe_a, dataframe_b):
            logging.error("DataFrames differ")
            return False

    if not values_equal(dataframe_a, dataframe_b, orderby):
        logging.error("DataFrames differ")
        return False

    logging.info("DataFrames are equal")
    return True

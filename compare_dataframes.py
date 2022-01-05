import logging
import numpy as np

logger = logging.getLogger(__name__)


def nrows_equal(a, b):

    nrowsa, _ = a.shape
    nrowsb, _ = b.shape

    if nrowsa == nrowsb:
        logger.info("Number of rows are equal {}".format(nrowsa))
        return True
    else:
        logger.warning("Number of rows differ {} vs {}".format(nrowsa, nrowsb))
        return False


def ncols_equal(a, b):

    _, ncolsa = a.shape
    _, ncolsb = b.shape

    if ncolsa == ncolsb:
        logger.info("Number of columns are equal {}".format(ncolsa))
        return True
    else:
        logger.warning("Number of columns differ {} vs {}".format(ncolsa, ncolsb))
        return False


def cols_equal(a, b):

    columnsa = a.columns
    columnsb = b.columns

    if np.array_equal(columnsa, columnsb):
        logger.info(f"Column names are equal")
        return True
    elif set(columnsa) == set(columnsb):
        logger.warning("Column names are equal but their order is different")
        return False
    else:
        logger.warning("Column names differ")
        return False


def dtypes_equal(a, b):

    dtypesa = a.dtypes
    dtypesb = b.dtypes

    if np.array_equal(dtypesa, dtypesb):
        logger.info("dtypes of columns are equal")
        return True
    else:
        logger.warning("dtypes of columns differ")
        return False


def values_equal(a, b, orderby):

    a = a.sort_values(by=orderby).reset_index()
    b = b.sort_values(by=orderby).reset_index()

    columns = []
    for c in a.columns:
        columns.append(a[c].equals(b[c]))

    if all(columns):
        logger.info("For every column all values are equal (up to row ordering)")
        return True
    else:
        columns = a.columns[columns==False]
        logger.info("Column(s): {columns} have differing values", columns)
        return False


def compare_dataframes(a, b, orderby):

    tests = [nrows_equal, ncols_equal, cols_equal, dtypes_equal]
    for test in tests:
        if not test(a, b):
            logging.error('DataFrames differ')
            return False
    logging.info('DataFrames are equal')
    return True


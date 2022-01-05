import logging
import numpy as np

logger = logging.getLogger(__name__)


def nrows_equal(a, b):

    nrowsa, _ = a.shape
    nrowsb, _ = b.shape

    if nrowsa == nrowsb:
        logger.info("Number of rows are equal %s", nrowsa)
        return True
    else:
        logger.warning("Number of rows differ %s vs %s", nrowsa, nrowsb)
        return False


def ncols_equal(a, b):

    _, ncolsa = a.shape
    _, ncolsb = b.shape

    if ncolsa == ncolsb:
        logger.info("Number of columns are equal %s", ncolsa)
        return True
    else:
        logger.warning("Number of columns differ %s vs %s", ncolsa, ncolsb)
        return False


def cols_equal(a, b):

    columnsa = a.columns
    columnsb = b.columns

    if np.array_equal(columnsa, columnsb):
        logger.info("Column names are equal")
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


def values_equal(a, b, orderby=None):
    
    if orderby:
        a = a.sort_values(by=orderby).reset_index(drop=True)
        b = b.sort_values(by=orderby).reset_index(drop=True)

    columns = []
    for c in a.columns:
        if a[c].dtype == np.float64:
            eq = np.allclose(a[c], b[c], rtol=1e-05, atol=1e-08, equal_nan=False)
        else:
            eq = np.array_equal(a[c].values, b[c].values, equal_nan=False)
        columns.append(eq)
        
        if eq == False and a[c].dtype == np.float64:
            print(c)
            print(a[a[c] != b[c]][c].head())
            print(b[a[c] != b[c]][c].head())

    if all(columns):
        logger.info("For every column all values are equal (up to row ordering)")
        return True
    else:                        
        logger.info("Columns %s have differing values", ', '.join(a.columns[columns]))
        return False


def compare_dataframes(a, b, orderby):

    tests = [nrows_equal, ncols_equal, cols_equal, dtypes_equal]
    for test in tests:
        if not test(a, b):
            logging.error('DataFrames differ')
            return False
        
    if not values_equal(a, b, orderby):
        logging.error('DataFrames differ')
        return False
    
    logging.info('DataFrames are equal')
    return True


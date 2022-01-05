#!/usr/bin/env python

import sys
import logging
import click

import pandas as pd

from compare_dataframes import compare_dataframes

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@click.group()
@click.command("file 1")
@click.option("--file1", type=click.Path(exists=True), help="path to file 1")
@click.command("file 2")
@click.option("--file2", type=click.Path(exists=True), help="path to file 2")
@click.command("orderby")
@click.option("--orderby", help="order dataframe by specified column")
def cli(file1, file2, orderby):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    compare_dataframes(df1, df2, orderby=orderby)


if __name__ == '__main__':
    cli()
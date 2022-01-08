#!/usr/bin/env python
"""Command-line tool to execute file comparison"""

import sys
import logging
import click

import pandas as pd

from src.checks import compare_dataframes

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@click.group()
@click.version_option("1.0.0")
def cli():
    """Compare two files for equality"""


@cli.command("compare")
@click.option("--file1", type=click.Path(exists=True), help="Path to file 1")
@click.option("--file2", type=click.Path(exists=True), help="Path to file 2")
@click.option(
    "--orderby",
    default=None,
    multiple=True,
    help="Optionally order dataframe by specified column",
)
def filediffer(file1, file2, orderby):
    """Check if two files are identical

    Args:
        file1 (string): file path to csv
        file2 (string): file path to csv
        orderby (string, optionally list of strings): reorder dataframes before checking
    """
    orderby = list(orderby)

    click.echo(click.style(f"Filename 1:{file1}"))
    click.echo(click.style(f"Filename 2:{file2}"))
    click.echo(click.style(f"orderby :{orderby}"))

    df1 = pd.read_csv(file1, low_memory=False)
    df2 = pd.read_csv(file2, low_memory=False)

    compare_dataframes(df1, df2, orderby=orderby)


if __name__ == "__main__":
    cli()

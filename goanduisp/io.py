"""
This module contains functions to manage user input/output.

Methods
-------
    get_file_name: ask for a file and return its path or exit if no file is selected
    import_df: import a DataFrame from a CSV or xlsx file
    info: return the info string
"""

import sys
from tkinter import filedialog
import pandas as pd
from .core import get_counts
from .version import __version_core__, __version_io__


def get_file_name() -> str:
    """
    Ask for a CSV file and return its path or exit if no file is selected.

    Returns
    -------
    str
        The path of the selected file.
    """
    file_name = filedialog.askopenfilename(
        title="Seleziona il file CSV da cui leggere i dati",
        filetypes=[("CSV files", "*.csv")],
    )
    if not file_name:
        print("Nessun file selezionato, esco.")
        input("Premi un tasto qualsiasi per chiudere...")
        sys.exit(0)
    return file_name


def import_df(file_name: str, header=0, sep=";") -> pd.DataFrame:
    """
    Import a DataFrame from a CSV or xslx file.

    Parameters
    ----------
    file_name : str
        The path of the file to import.

    Returns
    -------
    pd.DataFrame
        The imported DataFrame.
    """
    if file_name.endswith(".xlsx"):
        return pd.read_excel(file_name, header=header)
    else:
        return pd.read_csv(file_name, header=header, sep=sep)


def print_info(script: str, author: str, version: str) -> None:
    """
    Print the info string.

    Parameters
    ----------
    script : str
        The name of the script.
    author : str
        The name of the author.
    version : str
        The version of the script.

    Returns
    -------
    None
    """
    print(f"{script} by {author}, aggiornato al {version}")
    print(f"Basato su GOandUISP: core v{__version_core__} - io v{__version_io__}")


def print_counts(df: pd.DataFrame) -> None:
    """
    Print the the number of present athletes and the total number of athletes.
    Then, print the DataFrame with the counts of present and total athletes for each team.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame with the athletes data.

    Returns
    -------
    None
    """
    count_df = get_counts(df)
    print(f"Totale iscritti: {count_df["Totali"].sum()}")
    print(f"Totale presenti: {count_df["Presenti"].sum()}")
    print(count_df)

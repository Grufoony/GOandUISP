"""
This module contains functions to manage user input/output.

Methods
-------
    get_file_name: ask for a file and return its path or exit if no file is selected
    import_df: import a DataFrame from a CSV or xlsx file
"""

import sys
from tkinter import filedialog
import pandas as pd


def get_file_name(force_csv: bool = False) -> str:
    """
    Ask for a CSV file and return its path or exit if no file is selected.

    Returns
    -------
    str
        The path of the selected file.
    """
    if force_csv:
        file_types = [("CSV files", "*.csv")]
    else:
        file_types = [("Excel and CSV files", "*.xlsx *.csv")]
    file_name = filedialog.askopenfilename(
        title="Seleziona il file CSV da cui leggere i dati",
        filetypes=file_types,
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

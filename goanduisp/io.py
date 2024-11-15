"""
This module contains functions to manage user input/output.

Methods
-------
    get_csv_file_name: ask for a CSV file and return its path or exit if no file is selected
"""

import sys
from tkinter import filedialog


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

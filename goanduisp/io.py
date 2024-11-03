"""
This module contains functions to manage user input/output.

Methods
-------
    get_csv_file_name: ask for a CSV file and return its path or exit if no file is selected
"""

import sys
from tkinter import filedialog


def get_csv_file_name():
    RESPONSE = filedialog.askopenfilename(
        title="Seleziona il file CSV da cui leggere i dati",
        filetypes=[("CSV files", "*.csv")],
    )
    if not RESPONSE:
        print("Nessun file selezionato, esco.")
        input("Premi un tasto qualsiasi per chiudere...")
        sys.exit(0)
    return RESPONSE

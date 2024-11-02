"""
This module contains the pipeline useful to convert files from a YOUNG CHALLENGE event.
"""

import sys
from tkinter import filedialog
import numpy as np
import pandas as pd

sys.path.insert(1, ".")
# pylint: disable=wrong-import-position
from src import go_and_uisp as GOandUISP

# pylint: enable=wrong-import-position

__version__ = "2024.11.02"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"ASSIGN FOLLOWING SERIES AND LANES by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print(
        'Questo programma è stato creato per la manifestazione "YOUNG CHALLENGE", '
        "come utility per l'assegnazione delle batterie nelle gare a inseguimento.\n"
    )
    RESPONSE = filedialog.askopenfilename(
        title="Seleziona il file CSV da cui leggere i dati",
        filetypes=[("CSV files", "*.csv")],
    )
    if not RESPONSE:
        print("Nessun file selezionato, esco.")
        input("Premi un tasto qualsiasi per chiudere...")
        sys.exit(0)
    df = pd.read_csv(RESPONSE, sep=";")
    RESPONSE = int(input("Inserisci il seed per la generazione casuale: "))
    np.random.seed(RESPONSE)
    df = GOandUISP.assing_random_series_and_lanes(df, 7)

    df.to_csv("./batterie_inseguimento.csv", sep=";", index=False)
    print("File batterie_inseguimento.csv salvato correttamente.")
    input("Premi un tasto qualsiasi per chiudere...")

"""
This module contains the pipeline useful to manage ISB circuit races.
"""

import sys
import pandas as pd
from tkinter import filedialog

sys.path.insert(1, ".")
# pylint: disable=wrong-import-position
from src import go_and_uisp as GOandUISP

# pylint: enable=wrong-import-position

__version__ = "2024.11.30"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"BSL by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print("Questo programma è stato creato per le manifestazioni del circuito BSL.\n")
    # ask for file path with tkinter
    file_name = filedialog.askopenfilename(
        title="Seleziona il file CSV da cui leggere i dati", filetypes=[("CSV files", "*.csv")]
    )
    if not file_name:
        print("Nessun file selezionato, esco.")
        input("Premi un tasto qualsiasi per chiudere...")
        sys.exit(0)
    # read csv file prova.csv
    df = pd.read_csv(file_name, header=None, sep=";")
    df = GOandUISP.reformat(df)
    # drop all rows with A into Absent
    df = df[df["Boolean"].str.strip() == "T"]
    df = df.reset_index(drop=True)
    print(df)
    n_teams = int(input("Inserisci il numero di squadre (intero): "))
    seed = int(input("Inserisci il seed (intero): "))
    distance = int(input("Inserisci la distanza (intero): "))
    style = str(input("Inserisci lo stile (stringa compresa in [F, D, R, S, M]): "))
    style = style.upper().strip()
    print(f"Creo {n_teams} squadre casuali con seed {seed}, distanza {distance} e stile {style}.")
    # build random teams
    teams = GOandUISP.build_random_teams(df=df, n_teams=n_teams, seed=seed, distance=distance, style=style)
    print(teams)
    # save teams to csv
    teams.to_csv("./teams.csv", index=False, header=True)
    print("Salvato il file teams.csv nella cartella corrente.")
    input("Premi un tasto qualsiasi per chiudere...")

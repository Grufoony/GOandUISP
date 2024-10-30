"""
This module contains the pipeline useful to manage ISB circuit races.
"""

import pathlib
import sys
from tkinter import filedialog
import pandas as pd

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
    # search in folder . for teams.csv, if found, ask to import it
    if pathlib.Path("./teams.csv").exists():
        print("Trovato il file teams.csv nella cartella corrente.")
        if input("Vuoi importare le squadre da questo file? [s/n] ").lower() == "s":
            teams = pd.read_csv("teams.csv")
            print("Squadre importate correttamente.")
    else:
        # ask for file path with tkinter
        response = filedialog.askopenfilename(
            title="Seleziona il file CSV da cui leggere i dati",
            filetypes=[("CSV files", "*.csv")],
        )
        if not response:
            print("Nessun file selezionato, esco.")
            input("Premi un tasto qualsiasi per chiudere...")
            sys.exit(0)
        # read csv file prova.csv
        df = pd.read_csv(response, header=None, sep=";")
        df = GOandUISP.reformat(df)
        # drop all rows with A into Absent
        df = df[df["Boolean"].str.strip() == "T"]
        df = df.reset_index(drop=True)
        print(df)
        n_teams = int(input("Inserisci il numero di squadre (intero): "))
        seed = int(input("Inserisci il seed (intero): "))
        distance = int(input("Inserisci la distanza (intero): "))
        STYLE = (
            str(input("Inserisci lo stile (stringa compresa in [F, D, R, S, M]): "))
            .upper()
            .strip()
        )
        print(
            f"Creo {n_teams} squadre casuali con seme {seed} sul {STYLE}."
        )
        # build random teams
        teams = GOandUISP.build_random_teams(
            df=df, n_teams=n_teams, seed=seed, distance=distance, style=STYLE
        )
        print(teams)
        # save teams to csv
        teams.to_csv("./teams.csv", index=False, header=True)
        print("Salvato il file teams.csv nella cartella corrente.")
    response = filedialog.askopenfilename(
        title="Seleziona il file CSV da cui leggere i dati",
        filetypes=[("CSV files", "*.csv")],
    )
    df = pd.read_csv(response, sep=";")
    response = input(
        "Iserire le gare per iscrizioni individuali "
        "(stringa separata da virgole - Stili Possibili F D R S M): "
    )
    df = GOandUISP.generate_random_subscriptions_from_teams(
        teams, df, 2, 69, [race.strip().upper() for race in response.split(",")]
    )

    df.to_csv("./individual_subs.csv", index=False, header=True, sep=";")
    print("Salvato il file individual_subs.csv nella cartella corrente.")

    input("Premi un tasto qualsiasi per chiudere...")

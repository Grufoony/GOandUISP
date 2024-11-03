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

__version__ = "2024.11.03"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"BSL by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print("Questo programma è stato creato per le manifestazioni del circuito BSL.\n")
    print(
        "Per una breve guida, consulta il file README.md "
        "(online: https://github.com/Grufoony/GOandUISP/tree/main/races/bsl)."
    )

    SEED = None
    RESPONSE = "n"
    # search in folder . for teams.csv, if found, ask to import it
    if pathlib.Path("./teams.csv").exists():
        print("Trovato il file teams.csv nella cartella corrente.")
        RESPONSE = input("Vuoi importare le squadre da questo file? [s/n] ").lower()
        if RESPONSE.lower() == "s":
            teams = pd.read_csv("teams.csv")
            print("Squadre importate correttamente.")
    if RESPONSE.lower() == "n":
        # ask for file path with tkinter
        print(
            "Seleziona il file CSV contenente i risultati dai quali costruire le squadre."
        )
        RESPONSE = filedialog.askopenfilename(
            title="Seleziona il file CSV da cui leggere i dati",
            filetypes=[("CSV files", "*.csv")],
        )
        if not RESPONSE:
            print("Nessun file selezionato, esco.")
            input("Premi un tasto qualsiasi per chiudere...")
            sys.exit(0)
        # read csv file prova.csv
        df = pd.read_csv(RESPONSE, header=None, sep=";")
        df = GOandUISP.reformat(df)
        # drop all rows with A into Absent
        df = df[df["Boolean"].str.strip() == "T"]
        df = df.reset_index(drop=True)
        n = int(input("Inserisci il numero di squadre (intero): "))
        SEED = int(input("Inserisci il seed (intero): "))
        distance = int(input("Inserisci la distanza (intero): "))
        STYLE = (
            str(input("Inserisci lo stile (stringa compresa in [F, D, R, S, M]): "))
            .upper()
            .strip()
        )
        print(f"Creo {n} squadre casuali con seme {SEED} sul {STYLE}.")
        # build random teams
        teams = GOandUISP.build_random_teams(
            df=df, n_teams=n, seed=SEED, distance=distance, style=STYLE
        )
        print(teams)
        # save teams to csv
        teams.to_csv("./teams.csv", index=False, header=True)
        print("Salvato il file teams.csv nella cartella corrente.")

    RESPONSE = "s"
    if pathlib.Path("./individual_subs.csv").exists():
        print("Trovato il file individual_subs.csv nella cartella corrente.")
        RESPONSE = input(
            "Vuoi sovrascrivere il file individual_subs.csv? [s/n] "
        ).lower()
    if RESPONSE.lower() == "s":
        print(
            "Seleziona il file CSV del portale UISP contenente le iscrizioni alla gara."
        )
        RESPONSE = filedialog.askopenfilename(
            title="Seleziona il file CSV da cui leggere i dati",
            filetypes=[("CSV files", "*.csv")],
        )
        df = pd.read_csv(RESPONSE, sep=";")
        if SEED is None:
            SEED = int(input("Inserisci il seed (intero): "))
        n = int(input("Inserisci il numero di gare per atleta (intero): "))
        RESPONSE = input(
            "Iserire le gare per iscrizioni individuali "
            "(stringa separata da virgole - Stili Possibili [F, D, R, S, M]): "
        )
        df = GOandUISP.generate_random_subscriptions_from_teams(
            teams=teams,
            seed=SEED,
            possible_races=[race.strip().upper() for race in RESPONSE.split(",")],
            sub_df=df,
            n_races=n,
        )

        df.to_csv("./individual_subs.csv", index=False, header=True, sep=";")
        print("Salvato il file individual_subs.csv nella cartella corrente.")

    RESPONSE = "s"
    if pathlib.Path("./relay_subs.csv").exists():
        print("Trovato il file relay_subs.csv nella cartella corrente.")
        RESPONSE = input("Vuoi sovrascrivere il file relay_subs.csv? [s/n] ").lower()
    if RESPONSE.lower() == "s":
        if SEED is None:
            SEED = int(input("Inserisci il seed (intero): "))
        RESPONSE = input(
            "Iserire le gare per iscrizioni staffette "
            "(stringa separata da virgole - Stili Possibili [F, D, R, S, M]): "
        )
        df = GOandUISP.generate_relay_subscriptions_from_teams(
            teams=teams,
            possible_races=[
                race.strip().upper().replace("X", "x") for race in RESPONSE.split(",")
            ],
        )
        df.to_csv("./relay_subs.csv", index=False, header=True, sep=";")
        print("Salvato il file relay_subs.csv nella cartella corrente.")

    input("Premi un tasto qualsiasi per chiudere...")

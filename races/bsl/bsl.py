"""
Questo programma è stato creato per le manifestazioni del circuito BSL.
Per una breve guida, consulta il file README.md online:

https://github.com/Grufoony/GOandUISP/tree/main/races/bsl

Ultimo aggiornamento: 23/11/2024
    - Rinominato il file di output "relay-subs" in "iscrizioni-staffette"
        NOTA: il file iscrizioni delle staffette DEVE terminare con "-staffette.csv"

"""

import pathlib
from goanduisp.core import (
    reformat,
    build_random_teams,
    generate_random_subscriptions_from_teams,
    generate_relay_subscriptions_from_teams,
    STYLES,
)
from goanduisp.io import get_file_name, import_df, info

__version__ = "2024.11.23"
__author__ = "Gregorio Berselli"

OUT_TEAMS_FILE = "teams.csv"
OUT_SUBS_FILE = "individual_subs.csv"
OUT_RELAY_FILE = "iscrizioni-staffette.csv"

if __name__ == "__main__":
    print(info(__author__, __version__))
    print(__doc__)

    SEED = None
    RESPONSE = "n"
    TEAMS = None
    # search in folder . for OUT_TEAMS_FILE, if found, ask to import it
    if pathlib.Path(OUT_TEAMS_FILE).exists():
        print(f"Trovato il file {OUT_TEAMS_FILE} nella cartella corrente.")
        RESPONSE = input("Vuoi importare le squadre da questo file? [s/n] ").lower()
        if RESPONSE.lower() == "s":
            TEAMS = import_df(OUT_TEAMS_FILE)
            print("Squadre importate correttamente.")
    if RESPONSE.lower() == "n":
        # ask for file path with tkinter
        print(
            "Seleziona il file contenente i risultati GAS dai quali costruire le squadre."
        )
        df = import_df(get_file_name(), header=None)
        df = reformat(df, keep_valid_times=True)
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
        TEAMS = build_random_teams(
            df=df, n_teams=n, seed=SEED, distance=distance, style=STYLE
        )
        print(TEAMS)
        # save teams to csv
        TEAMS.to_csv(OUT_TEAMS_FILE, index=False, header=True, sep=";")
        print(f"Salvato il file {OUT_TEAMS_FILE} nella cartella corrente.")

    RESPONSE = "s"
    if pathlib.Path(OUT_SUBS_FILE).exists():
        print(f"Trovato il file {OUT_SUBS_FILE} nella cartella corrente.")
        RESPONSE = input(f"Vuoi sovrascrivere il file {OUT_SUBS_FILE}? [s/n] ").lower()
    if RESPONSE.lower() == "s":
        print(
            "Seleziona il file CSV del portale UISP contenente le iscrizioni alla gara."
        )
        df = import_df(get_file_name(force_csv=True))
        if SEED is None:
            SEED = int(input("Inserisci il seed (intero): "))
        n = int(input("Inserisci il numero di gare per atleta (intero): "))
        RESPONSE = input(
            "Iserire le gare per iscrizioni individuali "
            "(stringa separata da virgole - Stili Possibili [F, D, R, S, M]): "
        )
        df = generate_random_subscriptions_from_teams(
            teams=TEAMS,
            seed=SEED,
            possible_races=[race.strip().upper() for race in RESPONSE.split(",")],
            sub_df=df,
            n_races=n,
        )

        df.to_csv(OUT_SUBS_FILE, index=False, header=True, sep=";")
        print(f"Salvato il file {OUT_SUBS_FILE} nella cartella corrente.")

    RESPONSE = "s"
    if pathlib.Path(OUT_RELAY_FILE).exists():
        print(f"Trovato il file {OUT_RELAY_FILE} nella cartella corrente.")
        RESPONSE = input(f"Vuoi sovrascrivere il file {OUT_RELAY_FILE}? [s/n] ").lower()
    if RESPONSE.lower() == "s":
        if SEED is None:
            SEED = int(input("Inserisci il seed (intero): "))
        RESPONSE = input(
            "Iserire le gare per iscrizioni staffette "
            "(stringa separata da virgole - Stili Possibili [F, D, R, S, M]): "
        )
        possible_races = [
            race.strip().upper().replace("X", "x") for race in RESPONSE.split(",")
        ]
        possible_races = [
            f"{race.split()[0]} {STYLES[race.split()[1].upper()]}"
            for race in possible_races
        ]
        df = generate_relay_subscriptions_from_teams(
            teams=TEAMS,
            possible_races=possible_races,
        )
        df.to_csv(OUT_RELAY_FILE, index=False, header=True, sep=";")
        print(f"Salvato il file {OUT_RELAY_FILE} nella cartella corrente.")

    input("Premi un tasto qualsiasi per chiudere...")

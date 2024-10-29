"""
This module contains the pipeline useful to manage ISB circuit races.
"""

import sys
import pandas as pd

sys.path.insert(1, ".")
# pylint: disable=wrong-import-position
from src import go_and_uisp as GOandUISP

# pylint: enable=wrong-import-position

__version__ = "2024.11.29"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"ISB by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print("Questo programma è stato creato per le manifestazioni del circuito ISB.\n")
    # read csv file prova.csv
    df = pd.read_csv("./races/isb/prova.csv", header=None, sep=";")
    df = GOandUISP.reformat(df)
    # drop all rows with A into Absent
    df = df[df["Boolean"].str.strip() == "T"]
    df = df.reset_index(drop=True)
    print(df)
    # build random teams
    teams = GOandUISP.build_random_teams(df=df, n_teams=4, seed=42)
    print(teams)
    # save teams to csv
    teams.to_csv("./teams.csv", index=False, header=True)

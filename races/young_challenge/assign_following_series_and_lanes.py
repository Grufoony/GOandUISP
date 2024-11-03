"""
This module contains the pipeline useful to convert files from a YOUNG CHALLENGE event.
"""

import numpy as np
import pandas as pd
from goanduisp.core import assing_random_series_and_lanes
from goanduisp.io import get_csv_file_name
from goanduisp.version import __version_core__, __version_io__

__version__ = "2024.11.02"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(
        f"ASSIGN FOLLOWING SERIES AND LANES by {__author__}, aggiornato al {__version__}"
    )
    print(f"Basato su GOandUISP: core v{__version_core__} - io v{__version_io__}\n")
    print(
        'Questo programma è stato creato per la manifestazione "YOUNG CHALLENGE", '
        "come utility per l'assegnazione delle batterie nelle gare a inseguimento.\n"
    )
    df = pd.read_csv(get_csv_file_name(), sep=";")
    seed = int(input("Inserisci il seed per la generazione casuale: "))
    np.random.seed(seed)
    n_lower_lane = int(input("Inserisci il numero della corsia inferiore: "))
    n_series = int(input("Inserisci il numero della prima serie: "))
    df = assing_random_series_and_lanes(df, 7, n_lower_lane, n_series)

    df.to_csv("./batterie_inseguimento.csv", sep=";", index=False)
    print("File batterie_inseguimento.csv salvato correttamente.")
    input("Premi un tasto qualsiasi per chiudere...")

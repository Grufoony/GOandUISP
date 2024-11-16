"""
This script assign points in Sono Pronto races.
"""

from tkinter import filedialog
import pandas as pd
from goanduisp.core import reformat, assign_points_by_time
from goanduisp.io import get_file_name, import_df
from goanduisp.version import __version_core__, __version_io__

__version__ = "2024.11.15"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"BSL by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP: core v{__version_core__} - io v{__version_io__}\n")
    print("Questo programma è stato creato per le manifestazioni del circuito BSL.\n")
    print("Seleziona il file CSV contenente i risultati")
    df = import_df(get_file_name(), header=None)
    df = reformat(df=df, keep_valid_times=True)
    print("Seleziona la cartella contenente le tabelle tempi/punteggi")
    df = assign_points_by_time(df, filedialog.askdirectory())
    df.to_csv("points.csv", index=False, header=True, sep=";")
    print("Salvato il file points.csv nella cartella corrente.")
    input("Premi un tasto qualsiasi per chiudere...")

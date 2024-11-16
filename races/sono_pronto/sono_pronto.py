"""
Questo programma è stato creato per l'assegnazione dei punti nel circuito "Sono pronto".
"""

from tkinter import filedialog
from goanduisp.core import reformat, assign_points_by_time
from goanduisp.io import get_file_name, import_df, info

__version__ = "2024.11.15"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(info(__author__, __version__))
    print(__doc__)

    print("Seleziona il file CSV contenente i risultati")
    df = import_df(get_file_name(), header=None)
    df = reformat(df=df, keep_valid_times=True)
    print("Seleziona la cartella contenente le tabelle tempi/punteggi")
    df = assign_points_by_time(df, filedialog.askdirectory())
    df.to_csv("points.csv", index=False, header=True, sep=";")
    print("Salvato il file points.csv nella cartella corrente.")
    input("Premi un tasto qualsiasi per chiudere...")

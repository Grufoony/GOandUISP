"""
Questo programma è stato creato per la manifestazione "COMBINATA STILI".
"""

from goanduisp.core import groupdata
from goanduisp.io import print_info, print_counts, import_df, get_file_name

__version__ = "2023.11.08"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print_info("CombinataStili", __author__, __version__)
    print(__doc__)
    df = import_df(get_file_name())
    print_counts(df)
    df = groupdata(df)
    df.to_csv("results.csv", index=False, sep=";")
    print("I risultati sono stati salvati in results.csv")

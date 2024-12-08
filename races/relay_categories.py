"""
Questo programma riempie automaticamente la categoria nei file staffette se presente il file di iscrizioni individuali."
"""

from goanduisp.core import fill_categories
from goanduisp.io import print_info, get_file_name, import_df

__version__ = "2024.12.8"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print_info("Relay Categories", __author__, __version__)
    print(__doc__)
    print("Selezionare il file delle iscrizioni delle staffette.")
    df = import_df(get_file_name())
    print("Selezionare il file delle iscrizioni individuali.")
    df_data = import_df(get_file_name())
    df = fill_categories(df, df_data)
    df.to_csv("iscrizioni-staffette.csv", index=False, sep=";")

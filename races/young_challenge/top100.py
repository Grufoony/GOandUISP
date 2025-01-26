"""
Questo programma è stato creato per la manifestazione "YOUNG CHALLENGE".
"""

from goanduisp.core import groupdata
from goanduisp.io import print_info, print_counts, import_df, get_file_name

__version__ = "2024.12.7"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(print_info("YoungChallenge", __author__, __version__))
    print(__doc__)
    # ask for jolly count
    use_jolly = input("Vuoi considerare i jolly? [s/n] ").lower()
    df = import_df(get_file_name())
    print_counts(df)
    df = groupdata(df, by_points=True, use_jolly=use_jolly.strip() == "s")
    # print head(5) for each index
    print(df.groupby(["Categoria", "Sesso"]).apply(lambda x: x.head(5)))
    df.to_csv("results.csv", index=True, sep=";")
    print("I risultati sono stati salvati in results.csv")

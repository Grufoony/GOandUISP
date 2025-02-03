"""
Script per produrre la classifica squadre per una manifestazione.
"""

from goanduisp.core import shrink, rank_teams
from goanduisp.io import get_file_name, import_df, print_info

__version__ = "2025.2.3"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print_info("Rank Teams", __author__, __version__)
    print(__doc__)
    print("Seleziona il file contenente i risultati")
    df = import_df(get_file_name())
    df = shrink(df)
    use_jolly = input("Vuoi considerare i jolly? [s/n] ").lower().strip() == "s"
    df = rank_teams(df, use_jolly=use_jolly)
    df.to_csv(f"team_ranking{"_jolly" if use_jolly else ""}.csv", index=True, sep=";")

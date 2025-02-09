"""
Script per produrre la classifica squadre per una manifestazione.
"""

from goanduisp.core import shrink, rank_teams
from goanduisp.io import get_file_name, import_df, print_info

__version__ = "2025.2.9"
__author__ = "Gregorio Berselli"


def point_formula(point: int, jolly: int) -> int:
    return point * jolly if jolly > 0 else point


if __name__ == "__main__":
    print_info("Rank Teams", __author__, __version__)
    print(__doc__)
    print("Seleziona il file contenente i risultati")
    df = import_df(get_file_name())
    df = shrink(df)
    use_jolly = input("Vuoi considerare i jolly? [s/n] ").lower().strip() == "s"
    if use_jolly:
        df = rank_teams(df, point_formula=point_formula)
    else:
        df = rank_teams(df)
    file_name = f"team_ranking{"_jolly" if use_jolly else ""}.csv"
    df.to_csv(file_name, index=True, sep=";")
    print(f"Classifica squadre salvata in '{file_name}'")

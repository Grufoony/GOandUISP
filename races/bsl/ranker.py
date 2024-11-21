"""
Questo script crea la classifica delle squadre partecipanti alla manifestazione "BSL".

Ultimo aggiornamento: 21/04/2024
 - Aggiunta la stampa dei nomi delle squadre nel file di output "classifica.csv"
"""

from goanduisp.core import reformat, rank_teams
from goanduisp.io import get_file_name, import_df, info

__version__ = "21/04/2024"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(info(__author__, __version__))
    print(__doc__)
    print("Seleziona il file contenente i risultati")
    df_results = import_df(get_file_name(), header=None)
    df_results = reformat(df=df_results, keep_valid_times=True, drop_relay=False)
    print("Seleziona il file CSV contenente le squadre")
    df_results["Name"] = df_results["Name"].str.upper()
    df_teams = import_df(get_file_name(force_csv=True))
    # for each name in df_teams, check if it is in df_results
    # if yes, replace df_results["Team"] with df_teams["Team"]
    for _, row in df_teams.iterrows():
        mask = df_results["Name"].str.contains(row["Name"], case=False)
        df_results.loc[mask, "Team"] = row["Team"]
    df_results.to_csv("results.csv", index=False, header=True, sep=";")
    df_results = rank_teams(df=df_results, nbest=2)
    print(df_results)
    df_results.to_csv("classifica.csv", index=True, sep=";")

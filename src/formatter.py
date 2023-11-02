"""
This class contains the main function of the program, which communicates as io interface with
the user.

Attributes
----------
__version__ : tuple
    The version of the class.
__author__ : str
    The author of the class.

Methods
-------
convert_folder() -> None
    This function converts all suitable files in the current folder using the utils class.
"""

import os
import pandas as pd
from src import utils


def accumulate() -> None:
    """
    This function accumulates all suitable files in the current folder using the utils class.

    Parameters
    ----------

    Returns
    -------
    None
    """
    changed_files = []
    for f in os.listdir():
        if f.endswith(".xlsx") or f.endswith(".xls"):
            df = pd.read_excel(f, header=None)
            # check if the file has 20 or 21 columns
            if len(df.columns) < 20 or len(df.columns) > 21:
                print(
                    "Il file "
                    + f
                    + " non è formattato correttamente per l'accumulo e verrà saltato."
                )
                continue
            df = utils.reformat(df=df)
            utils.print_counts(df=df)
            input("Premi INVIO per continuare...")
            out = utils.groupdata(df=df)
            out.to_excel(f, index=False)
            if not f.endswith(".xlsx"):
                os.remove(f)
            print(f'Il file "{f}" è stato convertito con successo!')
            changed_files.append(f)
    if len(changed_files) == 0:
        print("Non ci sono file da accumulare nella cartella corrente.")
    else:
        print("I file accumulati sono: ")
        for f in changed_files:
            print(f)


def find_categories() -> None:
    """
    This function finds the categories of all suitable files in the current folder using the utils
    class.

    Parameters
    ----------

    Returns
    -------
    """
    changed_files = []
    for f in os.listdir():
        if "-staffette" in f:
            df = pd.read_csv(f, sep=";")
            df_data = pd.read_csv(f.replace("-staffette", ""), sep=";")
            # check if the file has 12 columns
            if len(df.columns) != 12:
                print(
                    f'Il file "{f}" non è formattato correttamente per la creazione automatica '
                    + "delle categorie e verrà saltato."
                )
                continue

            # drop last two cols
            df = df.drop(df.columns[-2:], axis=1)

            # glue together 'Cognome' and 'Nome' of df_data
            df_data["Nome"] = df_data["Cognome"] + " " + df_data["Nome"]
            # make 'Nome' column lowercase
            df_data["Nome"] = df_data["Nome"].str.lower()
            df_data["Nome"] = df_data["Nome"].str.strip()

            in_cols = [
                "Codice",
                "Societa",
                "Categoria",
                "Sesso",
                "Gara",
                "Tempo",
                "A0",
                "A1",
                "A2",
                "A3",
            ]
            df.columns = in_cols

            # clear column 'Categoria'
            df["Categoria"] = ""

            out_df = utils.fill_categories(df, df_data)

            df.insert(0, "CategoriaVera", out_df["Categoria"])

            out_cols = [
                "CategoriaVera",
                "Codice",
                "Societa",
                "Categoria",
                "Sesso",
                "Gara",
                "Tempo",
                "Atleta",
                "Atleta",
                "Atleta",
                "Atleta",
            ]
            df.columns = out_cols

            df.to_csv(f, sep=";", index=False)
            changed_files.append(f)

    if len(changed_files) == 0:
        print("Non ci sono file in cui creare le categorie nella cartella corrente.")
    else:
        print("I file con categorie generate automaticamente sono: ")
        for f in changed_files:
            print(f)

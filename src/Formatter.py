import os
import pandas as pd
import src.Utils as Utils

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
    This function converts all suitable files in the current folder using the Utils class.
"""


def accumulate() -> None:
    """
    This function converts all suitable files in the current folder using the Utils class.

    Parameters
    ----------

    Returns
    -------
    None
    """
    # print(
    #     "GOandUISP v"
    #     + ("".join(str(utils.__version__))).replace(",", ".")
    #     + " by "
    #     + utils.__author__
    #     + "."
    # )
    # print(
    #     "Per informazioni su come utilizzare il programma si consulti il repository"
    #     " GitHub: https://github.com/Grufoony/GOandUISP\n\n"
    # )
    for f in os.listdir():
        if f.endswith(".xlsx") or f.endswith(".xls"):
            df = pd.read_excel(f, header=None)
            # check if the file has 20 or 21 columns
            if len(df.columns) < 20 or len(df.columns) > 21:
                print("Il file " + f + " non è nel formato corretto, verrà saltato.")
                continue
            df = Utils.format(df=df)
            Utils.print_counts(df=df)
            input("Premi INVIO per continuare...")
            out = Utils.groupdata(df=df)
            out.to_excel(f, index=False)
            if not f.endswith(".xlsx"):
                os.remove(f)
            print("File " + f + " convertito con successo!")
    print("Tutti i file presenti nella cartella sono stati convertiti con successo!")


def find_categories() -> None:
    for file in os.listdir():
        if "-staffette" in file:
            df_staffette = pd.read_csv(file, sep=";")
            df_data = pd.read_csv(file.replace("-staffette", ""), sep=";")
            # check if the file has 12 columns
            if len(df_staffette.columns) != 12:
                print("Il file " + file + " non è nel formato corretto, verrà saltato.")
                continue

            # drop last two cols
            df_staffette = df_staffette.drop(df_staffette.columns[-2:], axis=1)

            # glue together 'Cognome' and 'Nome' of df_data
            df_data["Nome"] = df_data["Cognome"] + " " + df_data["Nome"]
            # make 'Nome' column lowercase
            df_data["Nome"] = df_data["Nome"].str.lower()
            df_data["Nome"] = df_data["Nome"].str.strip()

            IN_COLS = [
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
            df_staffette.columns = IN_COLS

            # clear column 'Categoria'
            df_staffette["Categoria"] = ""

            out_df = Utils.fill_categories(df_staffette, df_data)

            df_staffette.insert(0, "CategoriaVera", out_df["Categoria"])

            OUT_COLS = [
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
            df_staffette.columns = OUT_COLS

            df_staffette.to_csv("tests.csv", sep=";", index=False)

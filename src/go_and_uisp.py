"""
This class contains the functions to convert the data from the GOandSwim format to the UISP
format.

Attributes
----------
__version__ : tuple
    The version of the class.
__author__ : str
    The author of the class.
STYLES : dict
    A dictionary containing the styles' names.

Methods
-------
_split_names(full_name: str) -> tuple
    This function splits a full name into name and surname.
reformat(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame
    This function is the main function of the class.
    It takes a file name as input and returns a pandas dataframe.
    The output dataset has the correct column labels, the correct style names and the correct
    names format.
print_counts(df: pd.core.frame.DataFrame) -> None
    This function prints how many athletes are in each team and the total
    (partecipating medals).
groupdata(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame
    This function takes a dataframe as input and returns a new dataframe with the correct
    format.
fill_categories(df: pd.core.frame.DataFrame, data: pd.core.frame.DataFrame)
        -> pd.core.frame.DataFrame
    This function takes two dataframes as input and returns a new dataframe with the correct
    categories.
accumulate(counts: bool = True, points: bool = False, jolly: bool = False) -> None
    This function accumulates all suitable files in the current folder.
find_categories() -> None
    This function finds the categories of all suitable files in the current folder.
"""

import os
from datetime import datetime
import pandas as pd


__version__ = (1, 5, 0)
__author__ = "Gregorio Berselli"
# races dictionary: GoAndSwim -> dbMeeting
STYLES = {"F": "Delfino", "D": "Dorso", "R": "Rana", "S": "SL", "M": "M"}
CATEGORY_PRIORITIES = {
    "EC": 1,
    "EA": 2,
    "EB": 4,
    "R": 5,
    "J": 6,
    "A": 7,
}
CATEGORIES = {
    "M": {
        6: "G",
        7: "G",
        8: "G",
        9: "EC",
        10: "EB",
        11: "EB",
        12: "EA",
        13: "EA",
        14: "R",
        15: "R",
        16: "R",
        17: "J",
        18: "J",
        19: "A",
        20: "A",
        21: "A",
        22: "A",
        23: "A",
        24: "A",
        25: "A",
    },
    "F": {
        5: "G",
        6: "G",
        7: "G",
        8: "EC",
        9: "EB",
        10: "EB",
        11: "EA",
        12: "EA",
        13: "R",
        14: "R",
        15: "J",
        16: "J",
        17: "A",
        18: "A",
        19: "A",
        20: "A",
        21: "A",
        22: "A",
        23: "A",
        24: "A",
        25: "A",
    },
}


def get_category(sex: str, year: int) -> str:
    """
    This function returns the category given sex and year.
    """
    if datetime.now().month > 9:
        age = datetime.now().year + 1 - year
    else:
        age = datetime.now().year - year
    if sex.upper().strip() == "M":
        try:
            return CATEGORIES["M"][age]
        except KeyError:
            return "nan"
    try:
        return CATEGORIES["F"][age]
    except KeyError:
        return "nan"


def split_names(full_name: str) -> tuple:
    """
    This function splits a full name into name and surname.
    If the full name is composed by more than two words, it asks the user to insert the surname.
    If the input is void, it takes the first word as surname and the rest as name.
    If the input consists of only one char, it takes the first two words as surname and the rest.

    Parameters
    ----------
    full_name : str
        The full name to be splitted.

    Returns
    -------
    tuple
        A tuple containing the name and the surname.
    """
    full_name = full_name.upper()
    if len(full_name.split()) > 2:
        print("Inserisci i dati di " + str(full_name) + ": ")
        while True:
            surname = input("Inserisci il COGNOME: ").upper()
            if len(surname.split()) == 0:
                surname = full_name.split()[0]
                name = full_name.replace(surname + " ", "")
                break
            if len(surname.split()) == 1 and surname in full_name.split()[0]:
                surname = f"{full_name.split()[0]} {full_name.split()[1]}"
                name = full_name.replace(surname + " ", "")
                break
            if surname in full_name:
                name = full_name.replace(surname + " ", "")
                break
            print("COGNOME non presente nel nome, riprova: ")
        return name, surname

    name_column = full_name.split()
    return name_column[1], name_column[0]


def reformat(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    This function is the main function of the class.
    It takes a file name as input and returns a pandas dataframe.
    The output dataset has the correct column labels,the correct style names and the correct
    names format.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe to be converted.

    Returns
    -------
    pandas.core.frame.DataFrame
        The converted dataframe.
    """
    # drop relay races rows
    df = df.drop(df[df[2] == 0].index).reset_index(drop=True)
    # drop relay races names column, if exists
    if len(df.columns) == 21:
        df.drop(df.columns[1], axis=1, inplace=True)

    df.columns = (
        ["Name", "Year", "Sex", "Category", "Distance", "Style", "Team"]
        + [""] * 3
        + ["Time"]
        + [""] * 2
        + ["Boolean", "Absent"]
        + [""]
        + ["Points", "Double"]
        + [""] * 2
    )
    # check if style column is correct
    incorrect_styles = False
    for style in df.Style.unique():
        if style.split()[0] not in list(STYLES):
            incorrect_styles = True
            break

    if incorrect_styles:
        df.columns = (
            ["Name", "Year", "Sex", "Category", "Distance", "Team", "Style"]
            + [""] * 3
            + ["Time"]
            + [""] * 2
            + ["Boolean", "Absent"]
            + [""]
            + ["Points", "Double"]
            + [""] * 2
        )

    # strip spaces in some columns
    df["Name"] = df["Name"].str.strip()
    df["Team"] = df["Team"].str.strip()
    # replace double spaces with single space in names
    df["Name"] = df["Name"].str.replace("  ", " ")

    return df


def print_counts(df: pd.core.frame.DataFrame) -> None:
    """
    This function prints how many athletes are in each team and the total
    (partecipating medals).

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe with the data to be counted.

    Returns
    -------
    None
    """
    # now print how many athletes are in each team and the total (partecipating medals)
    counter_df = df.drop(df.loc[df["Absent"].str.strip() == "A"].index, inplace=False)
    counter_df = counter_df.groupby(["Name", "Year", "Sex", "Team"])[["Time"]].agg(list)

    print(counter_df.index.get_level_values("Team").value_counts())
    print("TOTALE ATLETI PARTECIPANTI: " + str(len(counter_df.index)))


def groupdata(
    df: pd.core.frame.DataFrame,
    by_points: bool = False,
    use_jolly: bool = False,
    out_df: pd.core.frame.DataFrame = None,
) -> pd.core.frame.DataFrame:
    """
    This function takes a dataframe as input and returns a new dataframe with the correct
    format.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe to be converted.
    by_points : bool, optional
        If True, the function returns a dataframe with the total points for each athlete,
        by default False
    use_jolly : bool, optional
        If True, the function uses the jolly points, by default False
    out_df : pandas.core.frame.DataFrame, optional
        A dataframe partially converted, by default None

    Returns
    -------
    pandas.core.frame.DataFrame
        The converted dataframe.
    """
    # keep only rows with boolean set to T (valid times) and strip spaces in style column
    df.drop(df.loc[df["Boolean"].str.strip() != "T"].index, inplace=True)
    df["Style"] = df["Style"].str.strip()
    # keeping only interesting data
    df = df[
        [
            "Name",
            "Year",
            "Sex",
            "Style",
            "Distance",
            "Category",
            "Time",
            "Team",
            "Points",
            "Double",
        ]
    ]
    # replacing style names
    df = df.replace({"Style": STYLES})
    df["Race"] = df["Distance"].astype(str) + " " + df["Style"]
    # groupby races and times, i.e. get unique athletes
    df = df.groupby(["Name", "Year", "Sex", "Category", "Team"])[
        ["Race", "Time", "Points", "Double"]
    ].agg(list)

    if out_df is None:
        # creates empty output database with columns' names
        out_columns = ["Cognome", "Nome", "Anno", "Sesso"]
        for i in range(df["Race"].apply(len).max()):
            out_columns.append("Gara" + str(i + 1))
            out_columns.append("Tempo" + str(i + 1))
        out_columns.append("Societa")
        out_df = pd.DataFrame(columns=out_columns)

        out_df["Anno"] = df.index.get_level_values("Year")
        out_df["Sesso"] = df.index.get_level_values("Sex")
        out_df["Societa"] = df.index.get_level_values("Team")

        # split name column into words and ask surname in input if the number of words
        # is greater than 2
        print("Se richiesto, inserire i COGNOMI degli atleti mancanti.")
        print(
            "Se nessun COGNOME viene inserito, verrà preso il primo nome come COGNOME."
        )
        print(
            "Se il COGNOME è composto da una sola lettera, verranno considerati i primi due nomi."
        )
        for index, full_name in enumerate(df.index.get_level_values("Name")):
            name, surname = split_names(full_name=full_name)
            out_df.loc[index, "Nome"] = name
            out_df.loc[index, "Cognome"] = surname

        for athlete_index, row in enumerate(df.itertuples()):
            for index, race in enumerate(zip(row.Race, row.Time)):
                out_df.loc[athlete_index, "Gara" + str(index + 1)] = race[0]
                out_df.loc[athlete_index, "Tempo" + str(index + 1)] = race[1]

    if by_points:
        out_df["PuntiTotali"] = 0
        out_df["Categoria"] = df.index.get_level_values("Category")
        for athlete_index, row in enumerate(df.itertuples()):
            i = 0
            for points, double in zip(row.Points, row.Double):
                double = double.replace(",", ".") if "," in str(double) else double
                i += int(points)
                if use_jolly and int(float(double)) == 2:
                    i += int(points)
            out_df.loc[athlete_index, "PuntiTotali"] = i

        # print athlete with more points for each category and sex
        # if there are more than one athlete with the same points, print the one with lowest SL time

        out_df["TempoStile"] = ""
        for row in out_df.itertuples():
            for i in range(1, df["Race"].apply(len).max() + 1):
                if "SL" in str(getattr(row, f"Gara{i}")):
                    out_df.at[row.Index, "TempoStile"] = getattr(row, f"Tempo{i}")
                    break

        print(
            out_df.groupby(["Categoria", "Sesso"])[
                ["Cognome", "Nome", "Societa", "PuntiTotali", "TempoStile"]
            ]
            .apply(
                lambda x: x.sort_values(
                    by=["PuntiTotali", "TempoStile"], ascending=[False, True]
                ).head(3)
            )
            .droplevel(2)
        )

        return (
            out_df.groupby(["Categoria", "Sesso"])[
                ["Cognome", "Nome", "Societa", "PuntiTotali", "TempoStile"]
            ]
            .apply(
                lambda x: x.sort_values(
                    by=["PuntiTotali", "TempoStile"], ascending=[False, True]
                )
            )
            .droplevel(2)
        )

    return out_df


def fill_categories(
    df: pd.core.frame.DataFrame, data: pd.core.frame.DataFrame
) -> pd.core.frame.DataFrame:
    """
    This function takes two dataframes as input and returns a new dataframe with the correct
    categories.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe to be converted.
    data : pandas.core.frame.DataFrame
        The dataframe with the data to be used to fill the categories.

    Returns
    -------
    pandas.core.frame.DataFrame
        The converted dataframe.
    """
    # drop last two cols
    df = df.drop(df.columns[-2:], axis=1)

    # glue together 'Cognome' and 'Nome' of data
    data["Nome"] = data["Cognome"] + " " + data["Nome"]
    # make 'Nome' column lowercase
    data["Nome"] = data["Nome"].str.lower()
    data["Nome"] = data["Nome"].str.strip()
    for row in df.itertuples():
        categories = []
        for i in range(4):
            col = f"A{i}"
            try:
                athlete = getattr(row, col)
            except AttributeError:
                continue
            if str(athlete) == "nan":
                continue
            athlete = athlete.lower().strip()
            # seach for athlete in data with the same CodSocieta
            societa = data.loc[data["CodSocietà"] == row.Codice]
            search = societa.loc[data["Nome"] == athlete]
            # if search is empty continue
            if search.empty:
                continue
            sex = search["Sesso"].values[0]
            year = search["Anno"].values[0]
            sex.lower().strip()
            category = get_category(sex, year)
            categories.append(category)

        # take the max category given CATEGORIES dict
        if len(categories) == 0:
            category = "nan"
        else:
            category = max(categories, key=lambda x: CATEGORY_PRIORITIES[x])

        df.at[row.Index, "CategoriaVera"] = category

    return df


def accumulate(counts: bool = True, points: bool = False, jolly: bool = False) -> None:
    """
    This function accumulates all suitable files in the current folder.

    Parameters
    ----------

    Returns
    -------
    None
    """
    changed_files = []
    for f in os.listdir():
        if (f.endswith(".xlsx") or f.endswith(".xls")) and not "ACCUMULO" in f:
            df = pd.read_excel(f, header=None)
            # check if the file has 20 or 21 columns
            if len(df.columns) < 20 or len(df.columns) > 21:
                print(
                    "Il file "
                    + f
                    + " non è formattato correttamente per l'accumulo e verrà saltato."
                )
                continue
            df = reformat(df=df)
            if counts:
                print_counts(df=df)
                input("Premi INVIO per continuare...")
            out = groupdata(df=df)
            out.to_excel(f"ACCUMULATO_{f}", index=False)
            if points:
                out2 = groupdata(df=df, by_points=points, use_jolly=jolly, out_df=out)
                out2.to_excel(
                    f'ACCUMULO_{f.replace(".xlsx", "")}_PUNTEGGI.xlsx', index=True
                )
            changed_files.append(f)
    if len(changed_files) == 0:
        print("Non ci sono file da accumulare nella cartella corrente.")
    else:
        print("I file accumulati sono: ")
        for f in changed_files:
            print(f)


def find_categories() -> None:
    """
    This function finds the categories of all suitable files in the current folder.
    It requires two files named "<name>-staffette-dbmeeting.csv" and "<name>-dbmeeting.csv" where
    "<name>" is the name of the meeting.
    It will create a new file named "<name>-staffette.csv" with the categories.

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

            df.columns = [
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

            df.insert(0, "CategoriaVera", "")

            out_df = fill_categories(df, df_data)

            out_df.columns = [
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

            out_df.to_csv(f.replace("-dbmeeting", ""), sep=";", index=False)
            changed_files.append(f)

    if len(changed_files) == 0:
        print("Non ci sono file in cui creare le categorie nella cartella corrente.")
    else:
        print("I file con categorie generate automaticamente sono: ")
        for f in changed_files:
            print(f)

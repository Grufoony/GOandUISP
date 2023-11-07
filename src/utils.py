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
ACCUMULATE_INPUT_COLUMNS : list
    A list containing the names of the columns of the input file.
ACCUMULATE_INPUT_COLUMNS_RELAYRACE : list
    A list containing the name sof the columns of the input file (relay races).

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
"""

import pandas as pd


__version__ = (1, 4, 2)
__author__ = "Gregorio Berselli"
# races dictionary: GoAndSwim -> dbMeeting
STYLES = {"F": "Delfino", "D": "Dorso", "R": "Rana", "S": "SL", "M": "M"}
CATEGORY_PRIORITIES = {
    "EC": 1,
    "EA1": 2,
    "EA2": 3,
    "EB1": 4,
    "EB2": 5,
    "R": 6,
    "J": 7,
    "A": 8,
}

ACCUMULATE_INPUT_COLUMNS = (
    ["Name", "Year", "Sex", "Category", "Distance", "Style", "Team"]
    + [""] * 3
    + ["Time"]
    + [""] * 2
    + ["Boolean", "Absent"]
    + [""]
    + ["Points", "Double"]
    + [""] * 2
)
ACCUMULATE_INPUT_COLUMNS_RELAYRACE = (
    ["Name", "Year", "Sex", "Category", "Distance", "Team", "Style"]
    + [""] * 3
    + ["Time"]
    + [""] * 2
    + ["Boolean", "Absent"]
    + [""]
    + ["Points", "Double"]
    + [""] * 2
)

MALE_CATEGORIES = {2006: "A", 2008: "J", 2011: "R"}

FEMALE_CATEGORIES = {2008: "A", 2010: "J", 2012: "R"}


def get_category(sex: str, year: int) -> str:
    """
    This function returns the category given sex and year.
    """
    if sex.lower().strip() == "m":
        for y, cat in MALE_CATEGORIES.items():
            if year < y:
                return cat
        return "nan"
    for y, cat in FEMALE_CATEGORIES.items():
        if year < y:
            return cat
    return "nan"


def split_names(full_name: str) -> tuple:
    """
    This function splits a full name into name and surname.
    If the full name is composed by more than two words,it asks the user to insert the surname.

    Parameters
    ----------
    full_name : str
        The full name to be splitted.

    Returns
    -------
    tuple
        A tuple containing the name and the surname.
    """
    if len(full_name.split()) > 2:
        print("Inserisci i dati di " + str(full_name) + ": ")
        while True:
            surname = input("Inserisci il COGNOME: ").upper()
            if surname in full_name.upper():
                name = full_name.upper().replace(surname + " ", "")
                break
            print("COGNOME non presente nel nome, riprova: ")
        return name, surname

    name_column = full_name.split()
    return name_column[1].upper(), name_column[0].upper()


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

    df.columns = ACCUMULATE_INPUT_COLUMNS
    # check if style column is correct
    incorrect_styles = False
    for style in df.Style.unique():
        if style.split()[0] not in list(STYLES):
            incorrect_styles = True
            break

    if incorrect_styles:
        df.columns = ACCUMULATE_INPUT_COLUMNS_RELAYRACE

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

    # get unique athletes
    athletes = df.index

    if out_df is None:
        # creates empty output database with columns' names
        out_columns = ["Cognome", "Nome", "Anno", "Sesso"]
        max_len = df["Race"].apply(len).max()
        for i in range(max_len):
            out_columns.append("Gara" + str(i + 1))
            out_columns.append("Tempo" + str(i + 1))
        out_columns.append("Societa")
        out_df = pd.DataFrame(columns=out_columns)

        out_df["Anno"] = df.index.get_level_values("Year")
        out_df["Sesso"] = df.index.get_level_values("Sex")
        out_df["Societa"] = df.index.get_level_values("Team")

        # split name column into words and ask surname in input if the number of words
        # is greater than 2
        for index, full_name in enumerate(athletes.get_level_values("Name")):
            name, surname = split_names(full_name=full_name)
            out_df.loc[index, "Nome"] = name
            out_df.loc[index, "Cognome"] = surname

        for athlete_index, row in enumerate(df.itertuples()):
            for race_index, race in enumerate(zip(row.Race, row.Time)):
                out_df.loc[athlete_index, "Gara" + str(race_index + 1)] = race[0]
                out_df.loc[athlete_index, "Tempo" + str(race_index + 1)] = race[1]

    if by_points:
        out_df["PuntiTotali"] = 0
        out_df["Categoria"] = df.index.get_level_values("Category")
        for athlete_index, row in enumerate(df.itertuples()):
            p = 0
            for points, double in zip(row.Points, row.Double):
                p += int(points)
                if use_jolly and int(double) == 2:
                    p += int(points)
            out_df.loc[athlete_index, "PuntiTotali"] = p

        # print athlete with more points for each category and sex
        # if there are more than one athlete with the same points, print the one with lowest SL time

        # temp_df = out_df.copy()
        out_df["TempoStile"] = ""
        for row in out_df.itertuples():
            for i in range(1, 5):
                if "SL" in str(getattr(row, f"Gara{i}")):
                    out_df.at[row.Index, "TempoStile"] = getattr(row, f"Tempo{i}")
                    break

        temp_df = out_df.groupby(["Categoria", "Sesso"])[
            ["Cognome", "Nome", "Societa", "PuntiTotali", "TempoStile"]
        ].apply(
            lambda x: x.sort_values(
                by=["PuntiTotali", "TempoStile"], ascending=[False, True]
            ).head(3)
        )

        # drop index 2
        temp_df = temp_df.droplevel(2)

        print(temp_df)

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
    for row in df.itertuples():
        categories = []
        for i in range(4):
            col = f"A{i}"
            athlete = getattr(row, col)
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

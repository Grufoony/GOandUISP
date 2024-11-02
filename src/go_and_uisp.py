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
import random
import pandas as pd


__version__ = (1, 5, 4)
__author__ = "Gregorio Berselli"
# races dictionary: GoAndSwim -> dbMeeting
STYLES = {"F": "Delfino", "D": "Dorso", "R": "Rana", "S": "SL", "M": "M"}
CATEGORY_PRIORITIES = {
    "G": 0,
    "EC": 1,
    "EA": 2,
    "EB": 3,
    "R14": 4,
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

GROUPBY_RESUME_COLUMNS = [
    "Cognome",
    "Nome",
    "Societa",
    "PuntiTotali",
    "GareDisputate",
    "TempoStile",
]
RELAY_SUBSCIPTION_COLUMNS_NO_DUP = [
    "Codice",
    "Societa",
    "Categoria",
    "Sesso",
    "Gara",
    "Tempo",
    "Atleta0",
    "Atleta1",
    "Atleta2",
    "Atleta3",
]
RELAY_SUBSCIPTION_COLUMNS = [
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
        + [""] * 2
        + ["SubTime", "Time"]
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
            + [""] * 2
            + ["SubTime", "Time"]
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
    of the effective athletes (for partecipating medals).

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
    counter_df_total = df.groupby(["Name", "Year", "Sex", "Team"])[["Time"]].agg(list)
    print("TOTALE ATLETI:\t" + str(len(counter_df_total.index)))
    print("TOTALE ATLETI PARTECIPANTI:\t" + str(len(counter_df.index)))

    counter_df = pd.concat(
        [
            counter_df.index.get_level_values("Team").value_counts(),
            counter_df_total.index.get_level_values("Team").value_counts(),
        ],
        axis=1,
    )
    counter_df.columns = ["Presenti", "Totali"]

    print(counter_df)


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
        The converted dataframe. This dataframe contains the following columns:
        - "Cognome"
        - "Nome"
        - "Anno"
        - "Sesso"
        - "Gara1"
        - "Tempo1"
        - "..."
        - "GaraN"
        - "TempoN"
        - "Societa"
        - "GareDisputate" (containing the number of played races)
        - "PuntiTotali" (if by_points is True)
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
            out_df.loc[athlete_index, "GareDisputate"] = index + 1

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
                [
                    "Cognome",
                    "Nome",
                    "Societa",
                    "PuntiTotali",
                    "GareDisputate",
                    "TempoStile",
                ]
            ]
            .apply(
                lambda x: x.sort_values(
                    by=["PuntiTotali", "TempoStile"], ascending=[False, True]
                ).head(3)
            )
            .droplevel(2)
        )

        return (
            out_df.groupby(["Categoria", "Sesso"])[GROUPBY_RESUME_COLUMNS]
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
    Moreover, it also prints the number of athletes in each team that do not compete in individual
    races.

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

    # create a count dict with CodSocieta as keys
    count_dict = {}
    counted = []
    for row in df.itertuples():
        categories = []
        for i in range(4):
            col = f"Atleta{i}"
            try:
                athlete = getattr(row, col)
            except AttributeError:
                continue
            if str(athlete) == "nan":
                continue
            athlete = athlete.lower().strip()
            # seach for athlete in data with the same CodSocieta
            search = data.loc[data["CodSocietà"] == row.Codice].loc[
                data["Nome"] == athlete
            ]
            # if search is empty continue
            if search.empty:
                if athlete not in counted:
                    try:
                        count_dict[row.Societa] += 1
                    except KeyError:
                        count_dict[row.Societa] = 1
                    counted.append(athlete)
                continue
            category = get_category(
                search["Sesso"].values[0].lower().strip(), search["Anno"].values[0]
            )
            categories.append(category)

        # take the max category given CATEGORIES dict
        if len(categories) == 0:
            category = "nan"
        else:
            category = max(categories, key=lambda x: CATEGORY_PRIORITIES[x])

        df.at[row.Index, "CategoriaVera"] = category

    if len(count_dict) > 0:
        for team, count in count_dict.items():
            print(
                f"ATTENZIONE: la società {team} ha {count} "
                + "atleti che non gareggiano in gare individuali."
            )
        print("\nIn particolare, gli atleti sono:")
        for athlete in counted:
            print(athlete)
        print("")

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

            df.columns = RELAY_SUBSCIPTION_COLUMNS_NO_DUP + [""] * 2

            df.insert(0, "CategoriaVera", "")

            out_df = fill_categories(df, df_data)

            out_df.columns = RELAY_SUBSCIPTION_COLUMNS

            out_df.to_csv(f.replace("-dbmeeting", ""), sep=";", index=False)
            changed_files.append(f)

    if len(changed_files) == 0:
        print("Non ci sono file in cui creare le categorie nella cartella corrente.")
    else:
        print("I file con categorie generate automaticamente sono: ")
        for f in changed_files:
            print(f)


def create_subsets(df: pd.DataFrame, n_teams: int) -> list:
    """
    Creates subsets of athletes from a DataFrame of
    athletes

    Args:
        df: A pandas DataFrame with at least "Sex" "Category" columns
        n_teams: A int representing the maximum length of a subset

    Returns:
        A list of subsets, where each subset is a DataFrame

    """

    array_df = []
    for _, sex_df in df.groupby("Sex"):
        for _, cat_df in sex_df.groupby("Category"):
            array_df.append(cat_df)

    subsets = []
    for temp_df in array_df:
        subsets += [
            temp_df.iloc[i : i + n_teams] for i in range(0, len(temp_df), n_teams)
        ]

    # glue together subsets with len < n_teams and subdivide them again
    sub_rest_m = [
        subset
        for subset in subsets
        if len(subset) < n_teams and subset["Sex"].values[0].strip() == "M"
    ]
    sub_rest_f = [
        subset
        for subset in subsets
        if len(subset) < n_teams and subset["Sex"].values[0].strip() == "F"
    ]
    subsets = [subset for subset in subsets if len(subset) == n_teams]
    if len(sub_rest_m) > 0:
        sub_rest_m = pd.concat(sub_rest_m)
        subsets += [
            sub_rest_m.iloc[i : i + n_teams] for i in range(0, len(sub_rest_m), n_teams)
        ]
    if len(sub_rest_f) > 0:
        sub_rest_f = pd.concat(sub_rest_f)
        subsets += [
            sub_rest_f.iloc[i : i + n_teams] for i in range(0, len(sub_rest_f), n_teams)
        ]

    return subsets


def build_random_teams(
    df: pd.DataFrame, n_teams: int, seed: int, distance: int = 50, style: str = "F"
) -> pd.DataFrame:
    """
    Builds random teams from a DataFrame of athletes and their race times.

    Args:
        df: A pandas DataFrame with columns "Name" and "Time".
        n_teams: The desired number of teams.

    Returns:
        A list of teams, where each team is a list of tuples (name, race_time).
    """
    # filter by distance and style
    df = df[
        (df["Distance"].astype(int) == distance) & (df["Style"].str.strip() == style)
    ]
    if df.empty:
        return pd.DataFrame()
    # keep only Name Time columns
    df = df[["Name", "Year", "Sex", "Category", "Time"]]
    # transform time column using time_to_int
    df["Time"] = df["Time"].apply(time_to_int)
    df = df.sort_values(by="Time")
    df["Time"] = df["Time"].apply(int_to_time)

    subsets = create_subsets(df, n_teams)

    # print("SUBSETS:")
    # for subset in subsets:
    #     print(subset)
    # init teams df
    teams = pd.DataFrame(columns=["Name", "Year", "Sex", "Time", "Team"])
    # TEAM NAMES CONSTANT (COLORS)
    team_names = [
        "Rosso",
        "Blu",
        "Verde",
        "Giallo",
        "Viola",
        "Arancione",
        "Bianco",
        "Nero",
    ]

    team_name_idx = 0
    # get the id in the subsets list of the df with Sex = F and len < n_teams
    id_len = (-1, -1)
    for i, subset in enumerate(subsets):
        if len(subset) < n_teams and subset["Sex"].values[0].strip() == "F":
            id_len = (i, n_teams - len(subset) - 1)
            break
    while len(subsets) > 0:
        for i, subset in enumerate(subsets):
            if (i, team_name_idx) == id_len:
                # Teams created firstly will have one more male
                # Teams created lastly will have one more female
                continue
            athlete = subset.sample(n=1, random_state=seed)
            athlete["Team"] = team_names[team_name_idx]
            teams = pd.concat([teams, athlete])

            # Directly modify the subset in-place
            subsets[i] = subset.drop(athlete.index)

        # remove empty subsets
        subsets = [subset for subset in subsets if not subset.empty]

        team_name_idx += 1

    # sort by time and groupby team
    teams = teams.groupby("Team").apply(
        lambda x: x.sort_values(by="Time"), include_groups=False
    )
    # reset index without dropping team column
    teams = teams.reset_index(level=1, drop=True)
    # transform index into a column
    teams = teams.reset_index()

    return teams


def time_to_int(time_str: str) -> int:
    """
    Converts a time string in the format '00'00"00' to an integer representing the time in
    centiseconds.

    Args:
        time_str: A time string in the format '00'00"00'.

    Returns:
        The time in centiseconds.
    """
    # ensure the string is stripped
    time_str = time_str.strip()
    # get data
    minutes = int(time_str[0:2])
    seconds = int(time_str[3:5])
    centiseconds = int(time_str[6:8])
    return minutes * 6000 + seconds * 100 + centiseconds


def int_to_time(time_int: int) -> str:
    """
    Converts an integer representing the time in centiseconds to a time string in the format
    '00'00"00'.

    Args:
        time_int: The time in centiseconds.

    Returns:
        The time string in the format '00'00"00'.
    """
    minutes = time_int // 6000
    seconds = (time_int % 6000) // 100
    centiseconds = time_int % 100
    return f"{minutes:02d}'{seconds:02d}\"{centiseconds:02d}"


def generate_random_subscriptions_from_teams(
    teams: pd.DataFrame,
    possible_races: list,
    seed: int,
    sub_df: pd.DataFrame,
    n_races: int,
) -> pd.DataFrame:
    """
    Generates random subscriptions for teams.

    Args:
        teams: A pandas teams DataFrame generated by build_random_teams function
        possible_races: A list of possible races to randomly assign to athletes
        seed: The seed for the random generator
        sub_df: A pandas DataFrame with the original subscriptions
        n_races: The number of races for each athlete

    Returns:
        A pandas DataFrame with the random subscriptions
    """

    random.seed(seed)

    # glue together 'Cognome' and 'Nome' of sub_df, uppering and stripping
    sub_df["Name"] = sub_df["Cognome"] + " " + sub_df["Nome"]
    sub_df["Name"] = sub_df["Name"].str.upper().str.strip()

    # remove from sub_df all athletes not in teams
    sub_df = sub_df[sub_df["Name"].isin(teams["Name"])].reset_index(drop=True)

    # Empty all columns named Gara1 Tempo1 Gara2 Tempo2 ...
    for i in range(1, n_races + 1):
        sub_df[f"Gara{i}"] = ""
        sub_df[f"Tempo{i}"] = ""
    for i in range(n_races + 1, sub_df.columns.str.contains("Gara").sum() + 1):
        sub_df.drop([f"Gara{i}", f"Tempo{i}"], axis=1, inplace=True)

    for _, athlete in teams.iterrows():
        athlete_id = sub_df.loc[sub_df["Name"] == athlete["Name"]].index[0]
        if athlete_id is None:
            print(f"Errore: atleta {athlete['Name']} non trovato.")
        for i, race in enumerate(random.sample(possible_races, n_races)):
            if athlete_id is None:
                print(
                    "Inserire maualmente l'iscrizione di "
                    f"{athlete['Name']} alla gara {race} con tempo {athlete['Time']}."
                )
            else:
                sub_df.at[athlete_id, f"Gara{i + 1}"] = race
                sub_df.at[athlete_id, f"Tempo{i + 1}"] = athlete["Time"]

    sub_df.drop(["Name"], axis=1, inplace=True)

    return sub_df


def generate_relay_subscriptions_from_teams(
    teams: pd.DataFrame, possible_races: list
) -> pd.DataFrame:
    """
    Generates relay subscriptions for teams.

    Args:
        teams: A pandas teams DataFrame generated by build_random_teams function
        possible_races: A list of possible races to randomly assign to relay teams

    Returns:
        A pandas DataFrame with the random subscriptions
    """
    sub_df = pd.DataFrame(columns=["CategoriaVera"] + RELAY_SUBSCIPTION_COLUMNS_NO_DUP)

    for team_name, team in teams.groupby("Team"):
        team = team.sort_values("Time")
        for race in possible_races:
            n_athletes = int(race.strip().split("x")[0])

            if n_athletes > sub_df.columns.str.contains("Atleta").sum():
                sub_df = sub_df.reindex(
                    columns=sub_df.columns.tolist()
                    + [
                        "Atleta{i}"
                        for i in range(
                            sub_df.columns.str.contains("Atleta").sum(),
                            n_athletes + 1,
                        )
                    ],
                    fill_value="",
                )

            # Create teams with equal gender distribution
            male_team = team[team["Sex"].str.strip() == "M"]
            female_team = team[team["Sex"].str.strip() == "F"]

            df = pd.DataFrame()
            # Combine male and female teams, alternating genders
            for i in range(
                min(len(male_team) // n_athletes, len(female_team) // n_athletes)
            ):

                df = pd.concat(
                    [
                        df,
                        male_team.iloc[i : i + n_athletes // 2],
                        female_team.iloc[i : i + n_athletes // 2],
                    ],
                    ignore_index=True,
                )
            for i in range(len(df) // n_athletes):
                # Create a list that will be the row
                # find max category
                row = [
                    max(
                        df["Category"].iloc[i * n_athletes : (i + 1) * n_athletes],
                        key=lambda x: CATEGORY_PRIORITIES[x.strip()],
                    )
                ]
                row += ["", team_name, row[0], "X", race]
                # tempo
                row.append(
                    int_to_time(
                        sum(
                            time_to_int(time)
                            for time in df["Time"].iloc[
                                i * n_athletes : (i + 1) * n_athletes
                            ]
                        )
                    )
                )
                # atleti
                row += df.iloc[i * n_athletes : (i + 1) * n_athletes]["Name"].tolist()
                if len(row) < len(sub_df.columns):
                    row += [""] * (len(sub_df.columns) - len(row))

                # append row to sub_df
                sub_df.loc[len(sub_df)] = row

    sub_df.columns = RELAY_SUBSCIPTION_COLUMNS + ["Atleta"] * (
        sub_df.columns.str.contains("Atleta").sum() - 4
    )

    return sub_df


def assing_random_series_and_lanes(
    sub_df: pd.DataFrame, n_athletes_per_team: int, n_lower_lane: int = 0
):
    """
    Generates random subscriptions

    """
    # append columns ["Serie", "Lane"] to sub_df
    sub_df["Serie", "Lane"] = ""

    n_serie = 0
    for i in range(n_athletes_per_team):
        # take the df composed of sub_df[0], sub_df[n_athletes_per_team],
        # sub_df[2*n_athletes_per_team], ...
        df = sub_df.iloc[i::n_athletes_per_team]
        # randomly shuffle the df
        df = df.sample(frac=1)
        # assign series and lanes like (0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), ...
        for j, index in enumerate(df.index):
            sub_df.at[index, "Serie"] = n_serie
            sub_df.at[index, "Lane"] = n_lower_lane + j % 4
            if j % 4 == 3 and not j == len(df) - 1:
                n_serie += 1
        n_serie += 1

    return sub_df

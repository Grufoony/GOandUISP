"""
This class contains the functions to convert the data from the GOandSwim format to the UISP
format.

Attributes
----------
STYLES : dict
    A dictionary containing the styles' names.

Methods
-------
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
"""

from datetime import datetime
import logging
import random
import pandas as pd

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
    "S": 7,
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
    sex = sex.upper().strip()
    try:
        categories = CATEGORIES[sex]
        return categories[age]
    except KeyError:
        max_age = max(categories.keys())
        if age > max_age:
            return categories[max_age]
        return "nan"


def shrink(df: pd.core.frame.DataFrame, keep_valid_times: bool = True):
    # Transform column Point2 in floats, given that they are numbers like 2,000
    df["Point2"] = df["Point2"].str.replace(",", ".").astype(float)
    df["Point"] = df["Point"].fillna(0)
    df["Point2"] = df["Point2"].fillna(0)
    if keep_valid_times:
        # keep only rows with RaceStatus equal to T
        df = df[df["RaceStatus"].str.strip() == "T"]

    return df


def get_counts(df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    This function takes a GAS results dataframe as input and returns a dataframe with two columns:
    the first one contains the number of present athletes and the second one the total number of subs.
    Rows are indexed by club names.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The GAS dataframe containing results.

    Returns
    -------
    pandas.core.frame.DataFrame
        The dataframe with the counts.
    """
    # now print how many athletes are in each team and the total (partecipating medals)
    counter_df = df.drop(
        df.loc[df["CalculationFlag"].str.strip() == "A"].index, inplace=False
    )
    counter_df = counter_df.groupby(["Fullname", "BirthYear", "Sex", "ClubName"])[
        ["RaceTime"]
    ].agg(list)
    counter_df_total = df.groupby(["Fullname", "BirthYear", "Sex", "ClubName"])[
        ["RaceTime"]
    ].agg(list)

    counter_df = pd.concat(
        [
            counter_df_total.index.get_level_values("ClubName").value_counts(),
            counter_df.index.get_level_values("ClubName").value_counts(),
        ],
        axis=1,
    )
    counter_df.columns = ["Iscritti", "Presenti"]

    return counter_df


def groupdata(
    df: pd.core.frame.DataFrame,
    by_points: bool = False,
    use_jolly: bool = False,
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
    df = shrink(df)
    # keeping only interesting data
    df = df[
        [
            "Name",
            "Surname",
            "BirthYear",
            "Sex",
            "StyleId",
            "Length",
            "CategoryId",
            "RaceTime",
            "ClubName",
            "Point",
            "Point2",
        ]
    ]
    # replacing style names
    df = df.replace({"StyleId": STYLES})
    df["Race"] = df["Length"].astype(str) + " " + df["StyleId"]
    # groupby races and times, i.e. get unique athletes
    df = df.groupby(["Name", "Surname", "BirthYear", "Sex", "CategoryId", "ClubName"])[
        ["Race", "RaceTime", "Point", "Point2"]
    ].agg(list)

    # creates empty output database with columns' names
    out_columns = ["Cognome", "Nome", "Anno", "Sesso"]
    for i in range(df["Race"].apply(len).max()):
        out_columns.append("Gara" + str(i + 1))
        out_columns.append("Tempo" + str(i + 1))
    out_columns.append("Societa")
    out_df = pd.DataFrame(columns=out_columns)

    out_df["Cognome"] = df.index.get_level_values("Surname")
    out_df["Nome"] = df.index.get_level_values("Name")
    out_df["Anno"] = df.index.get_level_values("BirthYear")
    out_df["Sesso"] = df.index.get_level_values("Sex")
    out_df["Societa"] = df.index.get_level_values("ClubName")

    for athlete_index, row in enumerate(df.itertuples()):
        for index, race in enumerate(zip(row.Race, row.RaceTime)):
            out_df.loc[athlete_index, "Gara" + str(index + 1)] = race[0]
            out_df.loc[athlete_index, "Tempo" + str(index + 1)] = race[1]
        out_df.loc[athlete_index, "GareDisputate"] = index + 1

    if by_points:
        out_df["PuntiTotali"] = 0
        out_df["Categoria"] = df.index.get_level_values("CategoryId")
        for athlete_index, row in enumerate(df.itertuples()):
            i = 0
            for points, double in zip(row.Point, row.Point2):
                i += int(points)
                if use_jolly and int(double) == 2:
                    i += int(points)
            out_df.loc[athlete_index, "PuntiTotali"] = i

        # print athlete with more points for each category and sex
        # if there are more than one athlete with the same points, print the one with lowest SL time

        out_df["TempoStile"] = ""
        for row in out_df.itertuples():
            for i in range(1, df["RaceTime"].apply(len).max() + 1):
                if "SL" in str(getattr(row, f"Gara{i}")):
                    out_df.at[row.Index, "TempoStile"] = getattr(row, f"Tempo{i}")
                    break

        return (
            out_df.groupby(["Categoria", "Sesso"])[GROUPBY_RESUME_COLUMNS]
            .apply(
                lambda x: x.sort_values(
                    by=["GareDisputate", "PuntiTotali", "TempoStile"],
                    ascending=[False, False, True],
                )
            )
            .droplevel(2)
        )

    return out_df


def rank_teams(
    df: pd.core.frame.DataFrame,
    point_formula=None,
    nbest: int = None,
) -> pd.core.frame.DataFrame:
    """
    This function takes a reformatted GAS result dataframe as input and returns the teams ranking.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe containing results.
    point_formula : function
        A function that takes Point and Point2 columns as input and computes the point value.
    use_jolly : bool, optional
        Whether to apply the jolly multiplier.
    nbest : int, optional
        If given, only the first nbest athletes will be counted for each Race, i.e.
        Distance-Style-Sex-Category combination.

    Returns
    -------
    pandas.core.frame.DataFrame
        The teams ranking dataframe.
    """
    # Keeping only relevant columns
    df = df[["Description", "RaceTime", "ClubName", "Point", "Point2"]]

    if point_formula is not None:
        # Apply point calculation formula
        df.loc[:, "Point"] = df.apply(
            lambda row: point_formula(row["Point"], row["Point2"]), axis=1
        )

    # Convert RaceTime to integer and sort
    df.loc[:, "RaceTime"] = df["RaceTime"].apply(time_to_int)
    df = df.sort_values(by="RaceTime")

    # Keep only top 'nbest' athletes per race and club
    if nbest is not None:
        df = df.groupby(["Description", "ClubName"]).head(nbest)

    # Aggregate points per team
    df = df.groupby("ClubName")["Point"].sum().sort_values(ascending=False)

    return df


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
    df.columns = RELAY_SUBSCIPTION_COLUMNS_NO_DUP + [""] * 2
    df.insert(0, "CategoriaVera", "")
    print(df)
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
            if category != "nan":
                categories.append(category)

        # take the max category given CATEGORIES dict
        if len(categories) != 0:
            category = max(categories, key=lambda x: CATEGORY_PRIORITIES[x])
        else:
            logging.warning(f"Non è stato possibile assegnare una categoria a {row}")

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

    df.columns = RELAY_SUBSCIPTION_COLUMNS

    return df


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
        for _, cat_df in sex_df.groupby("CategoryId"):
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
        (df["Length"].astype(int) == distance) & (df["StyleId"].str.strip() == style)
    ]
    if df.empty:
        return pd.DataFrame()
    # keep only Name Time columns
    df = df[["Fullname", "BirthYear", "Sex", "CategoryId", "RaceTime"]]
    # transform time column using time_to_int
    df["RaceTime"] = df["RaceTime"].apply(time_to_int)
    df = df.sort_values(by="RaceTime")
    df["RaceTime"] = df["RaceTime"].apply(int_to_time)

    subsets = create_subsets(df, n_teams)

    # init teams df
    teams = pd.DataFrame(
        columns=["Fullname", "BirthYear", "Sex", "RaceTime", "ClubName"]
    )
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
    # TODO: optimization algorithm:
    # - create an array to store the sum of times of each team you're creating
    # - initialize it as subset[0]
    # - for each subset, add the fastest athlete to the team with the higher sum and so on
    while len(subsets) > 0:
        for i, subset in enumerate(subsets):
            if (i, team_name_idx) == id_len:
                # Teams created firstly will have one more male
                # Teams created lastly will have one more female
                continue
            athlete = subset.sample(n=1, random_state=seed)
            athlete["ClubName"] = team_names[team_name_idx]
            teams = pd.concat([teams, athlete])

            # Directly modify the subset in-place
            subsets[i] = subset.drop(athlete.index)

        # remove empty subsets
        subsets = [subset for subset in subsets if not subset.empty]

        team_name_idx += 1

    # sort by time and groupby team
    teams = teams.groupby("ClubName").apply(
        lambda x: x.sort_values(by="RaceTime"), include_groups=False
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
    time_str = time_str.strip().replace("'", " ").replace('"', " ")
    # fill the string with 0s if it is too short
    if len(time_str) < 8:
        time_str = time_str.zfill(8)
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
    sub_df = sub_df[sub_df["Name"].isin(teams["Fullname"])].reset_index(drop=True)

    # Empty all columns named Gara1 Tempo1 Gara2 Tempo2 ...
    for i in range(1, n_races + 1):
        sub_df[f"Gara{i}"] = ""
        sub_df[f"Tempo{i}"] = ""
    for i in range(n_races + 1, sub_df.columns.str.contains("Gara").sum() + 1):
        sub_df.drop([f"Gara{i}", f"Tempo{i}"], axis=1, inplace=True)

    for _, athlete in teams.iterrows():
        try:
            athlete_id = sub_df.loc[sub_df["Name"] == athlete["Fullname"]].index[0]
        except IndexError:
            athlete_id = None
        if athlete_id is None:
            print(f"ATTENZIONE: atleta {athlete['Fullname']} non trovato.")
        else:
            sub_df.at[athlete_id, "Societa"] = athlete["ClubName"]
        for i, race in enumerate(random.sample(possible_races, n_races)):
            if athlete_id is None:
                print(
                    "Inserire maualmente l'iscrizione di "
                    f"{athlete["Fullname"]} alla gara {race} nella squadra {athlete["ClubName"]} con tempo {athlete["RaceTime"]}."
                )
            else:
                sub_df.at[athlete_id, f"Gara{i + 1}"] = race
                sub_df.at[athlete_id, f"Tempo{i + 1}"] = athlete["RaceTime"]

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

    for team_name, team in teams.groupby("ClubName"):
        team = team.sort_values("RaceTime")
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
                min(
                    len(male_team) // (n_athletes // 2),
                    len(female_team) // (n_athletes // 2),
                )
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
                        df["CategoryId"].iloc[i * n_athletes : (i + 1) * n_athletes],
                        key=lambda x: CATEGORY_PRIORITIES[x.strip()],
                    )
                ]
                row += ["", team_name, row[0], "X", race]
                # tempo
                row.append(
                    int_to_time(
                        sum(
                            time_to_int(time)
                            for time in df["RaceTime"].iloc[
                                i * n_athletes : (i + 1) * n_athletes
                            ]
                        )
                    )
                )
                # atleti
                row += df.iloc[i * n_athletes : (i + 1) * n_athletes][
                    "Fullname"
                ].tolist()
                if len(row) < len(sub_df.columns):
                    row += [""] * (len(sub_df.columns) - len(row))

                # append row to sub_df
                sub_df.loc[len(sub_df)] = row

    sub_df.columns = RELAY_SUBSCIPTION_COLUMNS + ["Atleta"] * (
        sub_df.columns.str.contains("Atleta").sum() - 4
    )

    sub_df["CategoriaVera"] = sub_df["CategoriaVera"].str.strip()
    sub_df["Categoria"] = sub_df["Categoria"].str.strip()

    return sub_df


def assing_random_series_and_lanes(
    sub_df: pd.DataFrame,
    n_athletes_per_team: int,
    n_lower_lane: int = 0,
    n_serie: int = 0,
):
    """
    Generates random series and lanes for a DataFrame of subscriptions.
    This is designed for a gara a inseguimento, in which the series are composed of four athletes
    from different teams, each one competing in a different style (assigned to the lane).

    Args:
        sub_df: A pandas DataFrame with the subscriptions
        n_athletes_per_team: The number of athletes per team
        n_lower_lane: The number of the lower lane
        n_serie: The number of the first serie

    Returns:
        sub_df with the columns "Serie" and "Lane" filled with the correct values

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


def assign_points_by_time(df: pd.DataFrame, data_folder: str) -> pd.DataFrame:
    """
    Assigns points to athletes based on their race time, using reference tables in CSV format.

    Args:
        df: A pandas DataFrame with the athletes and their
        data_folder: The folder containing the CSV files with the reference tables

    Returns:
        A pandas DataFrame with the athletes and their points
    """
    for _, row in df.iterrows():
        category = row["CategoryId"].strip().upper()
        distance = row["Length"]
        df_data = None
        if "C" in category or "B1" in category:
            df_data = pd.read_csv(f"{data_folder}/{distance}_c_b1.csv", sep=";")
        else:
            df_data = pd.read_csv(f"{data_folder}/{distance}.csv", sep=";")

        # put in row["Points"] the data_row["Points"] where t_min <= row["Time"] <= t_max
        for _, data_row in df_data.iterrows():
            if (
                time_to_int(data_row["t_min"])
                <= time_to_int(row["RaceTime"])
                <= time_to_int(data_row["t_max"])
            ):
                df.at[row.name, "Point"] = data_row["Point"]
                break

    return df

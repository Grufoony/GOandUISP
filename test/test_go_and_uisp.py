"""
This file contains the tests for the go_and_uisp.py module.
"""

from datetime import datetime
import pandas as pd
import numpy as np
import goanduisp.core as GOandUISP

NOW = datetime.now()
if NOW.month > 9:
    NOW = NOW.replace(year=NOW.year + 1)


def test_get_category_male():
    """
    This function tests the get_category function for male athletes.
    GIVEN a male athlete's sex and year of birth
    WHEN the function is called
    THEN it returns the correct category.
    """
    current_year = NOW.year
    assert GOandUISP.get_category("M", current_year - 20) == "A"
    assert GOandUISP.get_category("M", current_year - 18) == "J"
    assert GOandUISP.get_category("M", current_year - 16) == "R"
    assert GOandUISP.get_category("M", current_year - 14) == "R"
    assert GOandUISP.get_category("M", current_year - 12) == "EA"
    assert GOandUISP.get_category("M", current_year - 10) == "EB"
    assert GOandUISP.get_category("M", current_year - 9) == "EC"
    assert GOandUISP.get_category("M", current_year - 8) == "G"
    assert GOandUISP.get_category("M", current_year - 4) == "nan"


def test_get_category_female():
    """
    This function tests the get_category function for female athletes.
    GIVEN a female athlete's sex and year of birth
    WHEN the function is called
    THEN it returns the correct category.
    """
    current_year = NOW.year
    assert GOandUISP.get_category("F", current_year - 20) == "A"
    assert GOandUISP.get_category("F", current_year - 18) == "A"
    assert GOandUISP.get_category("F", current_year - 16) == "J"
    assert GOandUISP.get_category("F", current_year - 14) == "R"
    assert GOandUISP.get_category("F", current_year - 12) == "EA"
    assert GOandUISP.get_category("F", current_year - 9) == "EB"
    assert GOandUISP.get_category("F", current_year - 8) == "EC"
    assert GOandUISP.get_category("F", current_year - 7) == "G"
    assert GOandUISP.get_category("F", current_year - 3) == "nan"


def test_split_names():
    """
    This function tests the GOandUISP.split_names function.
    GIVEN a full name
    WHEN the function is called
    THEN it returns a tuple containing the name and the surname.
    """
    assert GOandUISP.split_names("Rossi Mario") == ("MARIO", "ROSSI")


def test_reformat():
    """
    This function tests the GOandUISP.reformat function.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the correct column labels, the correct style names and the
    correct names format.
    """
    data = {
        0: {
            0: "ROSSI MARIO ",
            1: "ROSSI MARIO ",
            2: "ROSSI  MARIO ",
            3: "ROSI MARIA ",
            4: "ROSI MARIA ",
        },
        1: {
            0: NOW.year - 11,
            1: NOW.year - 11,
            2: NOW.year - 11,
            3: NOW.year - 13,
            4: NOW.year - 13,
        },
        2: {0: " M ", 1: " M ", 2: " M ", 3: " F ", 4: " F "},
        3: {0: " EB1 ", 1: " EB1 ", 2: " EB1 ", 3: " EA2 ", 4: " EA2 "},
        4: {0: 50, 1: 100, 2: 200, 3: 100, 4: 100},
        5: {0: "F", 1: "D", 2: "R", 3: "S", 4: "M"},
        6: {0: " Aosta", 1: " Aosta", 2: " Aosta", 3: "Catanzaro", 4: "Catanzaro"},
        7: {0: 34, 1: 27, 2: 27, 3: 10, 4: 23},
        8: {0: 2, 1: 4, 2: 4, 3: 1, 4: 3},
        9: {
            0: " 00'45\"30 ",
            1: " 01'24\"50 ",
            2: " 01'24\"50 ",
            3: " 01'16\"00 ",
            4: " 01'24\"00 ",
        },
        10: {
            0: " 00'47\"10 ",
            1: " 01'24\"80 ",
            2: " 01'24\"80 ",
            3: " 01'17\"10 ",
            4: " 01'26\"90 ",
        },
        11: {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
        12: {0: 1, 1: 1, 2: 1, 3: 1, 4: 1},
        13: {0: " T ", 1: " T ", 2: " T ", 3: " S", 4: " T "},
        14: {0: "  ", 1: "  ", 2: "  ", 3: "  ", 4: "  "},
        15: {0: " EB1 ", 1: " EB1 ", 2: " EB1 ", 3: " EA2 ", 4: " EA2 "},
        16: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
        17: {0: 0, 1: 0, 2: 0, 3: 0, 4: 0},
        18: {0: "  ", 1: "  ", 2: "  ", 3: "  ", 4: "  "},
        19: {0: " ", 1: " ", 2: " ", 3: " ", 4: " "},
    }
    df = pd.DataFrame(data)
    out = GOandUISP.reformat(df)
    assert (set(out.Style.unique())) == set(GOandUISP.STYLES.keys())
    assert out["Name"].tolist() == [
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSI MARIA",
        "ROSI MARIA",
    ]
    assert set(out["Team"].tolist()) == set(["Aosta", "Catanzaro"])


def test_reformat2():
    """
    This function tests the GOandUISP.reformat function in the relay case.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the correct column labels, the correct style names and the
    correct names format.
    """
    data = {
        0: {
            0: "ROSSI MARIO ",
            1: "ROSSI MARIO ",
            2: "ROSSI  MARIO ",
            3: np.nan,
            4: "ROSI MARIA ",
            5: "ROSI MARIA ",
        },
        1: {0: np.nan, 1: np.nan, 2: np.nan, 3: "LOMBARDIA ASD", 4: np.nan, 5: np.nan},
        2: {
            0: NOW.year - 11,
            1: NOW.year - 11,
            2: NOW.year - 11,
            3: 0,
            4: NOW.year - 13,
            5: NOW.year - 13,
        },
        3: {0: " M ", 1: " M ", 2: " M ", 3: np.nan, 4: " F ", 5: " F "},
        4: {0: " EB1 ", 1: " EB1 ", 2: " EB1 ", 3: np.nan, 4: " EA2 ", 5: " EA2 "},
        5: {0: 50, 1: 100, 2: 200, 3: 100, 4: 100, 5: 100},
        6: {
            0: " Aosta",
            1: " Aosta",
            2: " Aosta",
            3: np.nan,
            4: "Catanzaro",
            5: "Catanzaro",
        },
        7: {0: "F", 1: "D", 2: "R", 3: "M", 4: "S", 5: "M"},
        8: {0: 34.0, 1: 27.0, 2: 27.0, 3: np.nan, 4: 10.0, 5: 23.0},
        9: {0: 2.0, 1: 4.0, 2: 4.0, 3: np.nan, 4: 1.0, 5: 3.0},
        10: {
            0: " 00'45\"30 ",
            1: " 01'24\"50 ",
            2: " 01'24\"50 ",
            3: "00'30'00",
            4: " 01'16\"00 ",
            5: " 01'24\"00 ",
        },
        11: {
            0: " 00'47\"10 ",
            1: " 01'24\"80 ",
            2: " 01'24\"80 ",
            3: "00'30\"00",
            4: " 01'17\"10 ",
            5: " 01'26\"90 ",
        },
        12: {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
        13: {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1},
        14: {0: " T ", 1: " T ", 2: " T ", 3: " T ", 4: " T ", 5: " T "},
        15: {0: "  ", 1: "  ", 2: "  ", 3: np.nan, 4: "  ", 5: "  "},
        16: {0: " EB1 ", 1: " EB1 ", 2: " EB1 ", 3: np.nan, 4: " EA2 ", 5: " EA2 "},
        17: {0: 0.0, 1: 0.0, 2: 0.0, 3: np.nan, 4: 0.0, 5: 0.0},
        18: {0: 0.0, 1: 0.0, 2: 0.0, 3: np.nan, 4: 0.0, 5: 0.0},
        19: {0: "  ", 1: "  ", 2: "  ", 3: np.nan, 4: "  ", 5: "  "},
        20: {0: " ", 1: " ", 2: " ", 3: np.nan, 4: " ", 5: " "},
    }
    df = pd.DataFrame(data)
    out = GOandUISP.reformat(df)
    assert (set(out.Style.unique())) == set(GOandUISP.STYLES.keys())
    assert out["Name"].tolist() == [
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSI MARIA",
        "ROSI MARIA",
    ]
    assert set(out["Team"].tolist()) == set(["Aosta", "Catanzaro"])


def test_groupdata1():
    """
    This function tests the GOandUISP.groupdata function when the athlets have same points.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the athlets sorted by time.
    """
    data = {
        "Name": ["Rossi Mario", "Rosi Luigi", "Rossi Mario"],
        "Year": [NOW.year - 14, NOW.year - 14, NOW.year - 14],
        "Sex": ["M", "M", "M"],
        "Team": ["Aosta", "Catanzaro", "Aosta"],
        "Style": ["SL", "SL", "Delfino"],
        "Distance": [100, 100, 100],
        "Category": ["A", "A", "A"],
        "Time": ["01'26\"45", "01'23\"45", "01'23\"45"],
        "Points": [1, 1, 0],
        "Double": ["0", "0", "0"],
        "Boolean": ["T", "T", "T"],
    }
    df = pd.DataFrame(data)
    out = GOandUISP.groupdata(df, by_points=True)
    assert out.columns.tolist() == GOandUISP.GROUPBY_RESUME_COLUMNS
    assert out.PuntiTotali.tolist() == [1, 1]
    assert out.TempoStile.tolist() == ["01'23\"45", "01'26\"45"]


def test_groupdata2():
    """
    This function tests the GOandUISP.groupdata function when the dataframe has only one row.
    GIVEN a dataframe with only one row
    WHEN the function is called
    THEN it returns a dataframe with the correct format.
    """
    data = {
        "Name": ["Rossi Mario"],
        "Year": [NOW.year - 14],
        "Sex": ["M"],
        "Team": ["Aosta"],
        "Style": ["Dorso"],
        "Distance": [100],
        "Category": ["A"],
        "Time": ["01'23\"45"],
        "Points": [1],
        "Double": ["0"],
        "Boolean": ["T"],
    }
    df = pd.DataFrame(data)
    out = GOandUISP.groupdata(df)
    assert out.columns.tolist() == [
        "Cognome",
        "Nome",
        "Anno",
        "Sesso",
        "Gara1",
        "Tempo1",
        "Societa",
        "GareDisputate",
    ]
    assert out.loc[0].tolist() == [
        "ROSSI",
        "MARIO",
        NOW.year - 14,
        "M",
        "100 Dorso",
        "01'23\"45",
        "Aosta",
        1,
    ]


def test_groupdata3():
    """
    This function tests the GOandUISP.groupdata function when the dataframe has multiple rows.
    GIVEN a dataframe with multiple rows
    WHEN the function is called
    THEN it returns a dataframe with the correct format.
    """
    data = {
        "Name": ["Rossi Mario", "Rosi Maria", "Rossi Mario"],
        "Year": [NOW.year - 14, NOW.year - 13, NOW.year - 14],
        "Sex": ["M", "F", "M"],
        "Team": ["Aosta", "Catanzaro", "Aosta"],
        "Style": ["Dorso", "Rana", "Delfino"],
        "Distance": [100, 200, 100],
        "Category": ["A", "B", "A"],
        "Time": ["01'23\"45", "01'23\"45", "01'23\"45"],
        "Points": [1, 2, 1],
        "Double": ["0", "0", "0"],
        "Boolean": ["T", "T", "T"],
    }
    df = pd.DataFrame(data)
    out = GOandUISP.groupdata(df)
    assert out.columns.tolist() == [
        "Cognome",
        "Nome",
        "Anno",
        "Sesso",
        "Gara1",
        "Tempo1",
        "Gara2",
        "Tempo2",
        "Societa",
        "GareDisputate",
    ]
    assert out.loc[0].tolist() == [
        "ROSI",
        "MARIA",
        NOW.year - 13,
        "F",
        "200 Rana",
        "01'23\"45",
        np.nan,
        np.nan,
        "Catanzaro",
        1,
    ]
    assert out.loc[1].tolist() == [
        "ROSSI",
        "MARIO",
        NOW.year - 14,
        "M",
        "100 Dorso",
        "01'23\"45",
        "100 Delfino",
        "01'23\"45",
        "Aosta",
        2,
    ]


def test_groupdata4():
    """
    This function tests the GOandUISP.groupdata function when by_points is True.
    GIVEN a dataframe and by_points is True
    WHEN the function is called
    THEN it returns a dataframe with the correct format.
    """
    data = {
        "Name": ["Rossi Mario", "Rosi Maria", "Rossi Mario"],
        "Year": [NOW.year - 14, NOW.year - 14, NOW.year - 14],
        "Sex": ["M", "F", "M"],
        "Team": ["Aosta", "Catanzaro", "Aosta"],
        "Style": ["Dorso", "Rana", "Delfino"],
        "Distance": [100, 200, 100],
        "Category": ["A", "B", "A"],
        "Time": ["01'23\"45", "01'23\"45", "01'23\"45"],
        "Points": [1, 2, 1],
        "Double": ["0", "0", "0"],
        "Boolean": ["T", "T", "T"],
    }
    df = pd.DataFrame(data)
    out = GOandUISP.groupdata(df, by_points=True)
    assert out.columns.tolist() == GOandUISP.GROUPBY_RESUME_COLUMNS
    assert out.PuntiTotali.tolist() == [2, 2]


def test_print_counts(capfd):
    """
    This function tests the GOandUISP.print_counts function.
    GIVEN a dataframe
    WHEN the function is called
    THEN it prints how many athletes are in each team and the total (partecipating medals).
    """
    # create a test dataframe
    data = {
        "Name": ["Rossi Mario", "Rosi Maria", "Rossi Mario", "Bianchi Giovanni"],
        "Year": [NOW.year - 14, NOW.year - 14, NOW.year - 13, NOW.year - 13],
        "Sex": ["M", "F", "M", "M"],
        "Team": ["Aosta", "Catanzaro", "Aosta", "Aosta"],
        "Time": ["01:23:45", "01:23:45", "01:23:45", "01:23:45"],
        "Absent": ["", "", "", "A"],
    }
    df = pd.DataFrame(data)

    # call the function
    GOandUISP.print_counts(df)

    # capture stdout
    out = capfd.readouterr()

    # check the output
    assert (
        out.out
        == "TOTALE ATLETI:\t4\nTOTALE ATLETI PARTECIPANTI:\t3\n           Presenti  Totali\nTeam"
        + "                       \nAosta             2       3\nCatanzaro         1       1\n"
    )


def test_fill_categories(capfd):
    """
    This function tests the GOandUISP.fill_categories function.
    GIVEN a dataframe and a data dataframe
    WHEN the function is called
    THEN it returns a dataframe with the correct categories.
    """
    # create a test dataframe
    data = {
        "CodSocietà": [1, 1, 2],
        "Cognome": ["Rossi", "Rosi", "Rosi"],
        "Nome": ["Mario", "Luigi", "Maria"],
        "Anno": [NOW.year - 14, NOW.year - 24, NOW.year - 16],
        "Sesso": ["M", "M", "F"],
    }
    df_data = pd.DataFrame(data)

    data = {
        "Codice": [1, 2],
        "Societa": ["Aosta", "Catanzaro"],
        "Categoria": ["", ""],
        "Sesso": ["M", "F"],
        "Gara": ["100 Dorso", "100 Dorso"],
        "Tempo": ["01'23\"45", "01'23\"45"],
        "Atleta0": ["Rossi Mario", "Rosi Maria"],
        "Atleta1": ["Rosi Luigi", "Zazza Alex"],
        "Atleta2": ["Gialli Fabio", np.nan],
        "Atleta3": [np.nan, np.nan],
        "Atleta4": [np.nan, np.nan],
        "Atleta5": [np.nan, np.nan],
    }
    df = pd.DataFrame(data)

    out = GOandUISP.fill_categories(df, df_data)
    out_line = capfd.readouterr()
    assert out.CategoriaVera.tolist() == ["A", "J"]
    assert (
        out_line.out
        == "ATTENZIONE: la società Aosta ha 1 atleti che non gareggiano in gare individuali."
        + "\nATTENZIONE: la società Catanzaro ha 1 atleti che non gareggiano in gare individuali.\n"
        + "\nIn particolare, gli atleti sono:\ngialli fabio\nzazza alex\n\n"
    )


def test_time_conversions():
    """
    This function tests the GOandUISP.time_to_int and GOandUISP.int_to_time functions.
    GIVEN a time in string or int format
    WHEN the time_to_int or int_to_time function is called
    THEN it returns the time in integer or string format
    """
    str_time = "00'00\"99"
    int_time = 99
    assert GOandUISP.time_to_int(str_time) == int_time
    assert GOandUISP.int_to_time(int_time) == str_time
    str_time = "00'59\"99"
    int_time = 5999
    assert GOandUISP.time_to_int(str_time) == int_time
    assert GOandUISP.int_to_time(int_time) == str_time
    str_time = "59'59\"99"
    int_time = 359999
    assert GOandUISP.time_to_int(str_time) == int_time
    assert GOandUISP.int_to_time(int_time) == str_time


def test_build_random_teams():
    """
    This function tests the GOandUISP.build_random_teams function.
    GIVEN a dataframe of athletes and their race times
    WHEN the function is called
    THEN it returns a dataframe with the athletes divided into random teams.
    """
    data = {
        "Name": [
            "Rossi Mario",
            "Rosi Luigi",
            "Bianchi Giovanni",
            "Verdi Luca",
            "Neri Marco",
        ],
        "Year": [
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
        ],
        "Sex": ["M", "M", "M", "M", "M"],
        "Category": ["A", "A", "A", "A", "A"],
        "Distance": [50, 50, 50, 50, 50],
        "Style": ["F", "F", "F", "F", "F"],
        "Time": ["00'30\"00", "00'31\"00", "00'32\"00", "00'33\"00", "00'34\"00"],
    }
    df = pd.DataFrame(data)
    n_teams = 2
    seed = 42
    teams = GOandUISP.build_random_teams(df, n_teams, seed)
    assert teams.columns.tolist() == ["Team", "Name", "Year", "Sex", "Time", "Category"]
    assert len(teams["Team"].unique()) == n_teams
    assert teams["Team"].value_counts().tolist() == [3, 2]


def test_build_random_teams_with_different_styles():
    """
    This function tests the GOandUISP.build_random_teams function with different styles.
    GIVEN a dataframe of athletes with different styles
    WHEN the function is called
    THEN it returns a dataframe with the athletes divided into random teams.
    """
    data = {
        "Name": [
            "Rossi Mario",
            "Rosi Luigi",
            "Bianchi Giovanni",
            "Verdi Luca",
            "Neri Marco",
        ],
        "Year": [
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
        ],
        "Sex": ["M", "M", "M", "M", "M"],
        "Category": ["A", "A", "A", "A", "A"],
        "Distance": [50, 50, 50, 50, 50],
        "Style": ["D", "D", "R", "S", "M"],
        "Time": ["00'30\"00", "00'31\"00", "00'32\"00", "00'33\"00", "00'34\"00"],
    }
    df = pd.DataFrame(data)
    n_teams = 2
    seed = 42
    teams = GOandUISP.build_random_teams(df, n_teams, seed, style="F")
    assert teams.empty  # No teams should be formed as no athlete matches the style "F"


def test_build_random_teams_with_different_distances():
    """
    This function tests the GOandUISP.build_random_teams function with different distances.
    GIVEN a dataframe of athletes with different distances
    WHEN the function is called
    THEN it returns a dataframe with the athletes divided into random teams.
    """
    data = {
        "Name": [
            "Rossi Mario",
            "Rosi Luigi",
            "Bianchi Giovanni",
            "Verdi Luca",
            "Neri Marco",
        ],
        "Year": [
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
        ],
        "Sex": ["M", "M", "M", "M", "M"],
        "Category": ["A", "A", "A", "A", "A"],
        "Distance": [100, 100, 100, 100, 100],
        "Style": ["F", "F", "F", "F", "F"],
        "Time": ["00'30\"00", "00'31\"00", "00'32\"00", "00'33\"00", "00'34\"00"],
    }
    df = pd.DataFrame(data)
    n_teams = 2
    seed = 42
    teams = GOandUISP.build_random_teams(df, n_teams, seed, distance=50)
    assert (
        teams.empty
    )  # No teams should be formed as no athlete matches the distance 50


def test_build_random_teams_with_mixed_sex():
    """
    This function tests the GOandUISP.build_random_teams function with mixed sex.
    GIVEN a dataframe of athletes with mixed sex
    WHEN the function is called
    THEN it returns a dataframe with the athletes divided into random teams.
    """
    data = {
        "Name": [
            "Rossi Mario",
            "Rosi Luigi",
            "Bianchi Giovanni",
            "Verdi Luca",
            "Neri Marco",
            "Bianchi Maria",
        ],
        "Year": [
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
            NOW.year - 14,
        ],
        "Sex": ["M", "M", "M", "M", "M", "F"],
        "Category": ["A", "A", "A", "A", "A", "A"],
        "Distance": [50, 50, 50, 50, 50, 50],
        "Style": ["F", "F", "F", "F", "F", "F"],
        "Time": [
            "00'30\"00",
            "00'31\"00",
            "00'32\"00",
            "00'33\"00",
            "00'34\"00",
            "00'35\"00",
        ],
    }
    df = pd.DataFrame(data)
    n_teams = 2
    seed = 42
    teams = GOandUISP.build_random_teams(df, n_teams, seed)
    assert teams.columns.tolist() == ["Team", "Name", "Year", "Sex", "Time", "Category"]
    assert len(teams["Team"].unique()) == n_teams
    assert teams["Team"].value_counts().tolist() == [3, 3]

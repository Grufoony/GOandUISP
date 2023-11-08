"""
This file contains the tests for the GOandUISP.py module.
"""

import pandas as pd
import numpy as np
from src import go_and_uisp as GOandUISP


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
    df = pd.read_excel("datasets/reformat_test.xlsx", header=None)
    out = GOandUISP.reformat(df)
    assert out.columns.tolist() == GOandUISP.ACCUMULATE_INPUT_COLUMNS
    assert (set(out.Style.unique())) == set(GOandUISP.STYLES.keys())
    assert out["Name"].tolist() == [
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSI MARIA",
        "ROSI MARIA",
    ]
    assert set(out["Team"].tolist()) == set(["Aosta", "Catanzaro"])


def test_reformat_relay():
    """
    This function tests the GOandUISP.reformat function in the relay case.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the correct column labels, the correct style names and the
    correct names format.
    """
    df = pd.read_excel("datasets/reformat_relay_test.xlsx", header=None)
    out = GOandUISP.reformat(df)
    assert out.columns.tolist() == GOandUISP.ACCUMULATE_INPUT_COLUMNS_RELAYRACE
    assert (set(out.Style.unique())) == set(GOandUISP.STYLES.keys())
    assert out["Name"].tolist() == [
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSSI MARIO",
        "ROSI MARIA",
        "ROSI MARIA",
    ]
    assert set(out["Team"].tolist()) == set(["Aosta", "Catanzaro"])


def test_print_counts(capfd):
    """
    This function tests the GOandUISP.print_counts function.
    GIVEN a dataframe
    WHEN the function is called
    THEN it prints how many athletes are in each team and the total (partecipating medals).
    """
    df = pd.read_excel("datasets/print_counts_test.xlsx", header=None)
    out = GOandUISP.reformat(df)
    GOandUISP.print_counts(out)
    out, _ = capfd.readouterr()
    assert (
        out
        == "Team\nAosta        3\nCatanzaro    1\nName: count"
        + ", dtype: int64\nTOTALE ATLETI PARTECIPANTI: 4\n"
    )


def test_groupdata1():
    """
    This function tests the GOandUISP.groupdata function.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the correct format.
    """
    df = pd.read_excel("datasets/reformat_test.xlsx", header=None)
    out = GOandUISP.reformat(df)
    out = GOandUISP.groupdata(out)
    assert out.columns.tolist() == [
        "Cognome",
        "Nome",
        "Anno",
        "Sesso",
        "Gara1",
        "Tempo1",
        "Gara2",
        "Tempo2",
        "Gara3",
        "Tempo3",
        "Societa",
    ]
    assert out.loc[0].tolist() == [
        "ROSI",
        "MARIA",
        2011,
        " F ",
        "100 M",
        " 01'26\"90 ",
        np.nan,
        np.nan,
        np.nan,
        np.nan,
        "Catanzaro",
    ]
    assert out.loc[1].tolist() == [
        "ROSSI",
        "MARIO",
        2013,
        " M ",
        "50 Delfino",
        " 00'47\"10 ",
        "100 Dorso",
        " 01'24\"80 ",
        "200 Rana",
        " 01'24\"80 ",
        "Aosta",
    ]


def test_groupdata2():
    """
    This function tests the GOandUISP.groupdata function when the athlets have same points.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the athlets sorted by time.
    """
    df = pd.read_excel("datasets/groupby_test.xlsx", header=None)
    df = GOandUISP.reformat(df)
    out = GOandUISP.groupdata(df, by_points=True, use_jolly=True)
    assert out.columns.tolist() == [
        "Cognome",
        "Nome",
        "Societa",
        "PuntiTotali",
        "TempoStile",
    ]
    assert out.PuntiTotali.tolist() == [70, 70]
    assert out.TempoStile.tolist() == [
        " 01'22\"80 ",
        " 01'26\"90 ",
    ]


def test_fill_categories():
    """
    This function tests the GOandUISP.fill_categories function.
    GIVEN a dataframe
    WHEN the function is called
    THEN it returns a dataframe with the correct categories.
    """
    df = pd.read_csv("datasets/fill_categories-staffette.csv", sep=";")
    df_data = pd.read_csv("datasets/fill_categories.csv", sep=";")

    # glue together 'Cognome' and 'Nome' of df_data
    df_data["Nome"] = df_data["Cognome"] + " " + df_data["Nome"]
    # make 'Nome' column lowercase
    df_data["Nome"] = df_data["Nome"].str.lower()
    df_data["Nome"] = df_data["Nome"].str.strip()

    out = GOandUISP.fill_categories(df, df_data)
    assert out["CategoriaVera"].values[0] == "A"

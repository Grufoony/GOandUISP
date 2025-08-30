"""
This file contains the tests for the go_and_uisp.py module.
"""

from datetime import datetime
import pandas as pd
from goanduisp.core import get_category, shrink, get_counts

NOW = datetime.now()
if NOW.month > 9:
    NOW = NOW.replace(year=NOW.year + 1)
INPUT_DATASET = pd.read_csv("./test/synthetic_race_data.csv", sep=";")


def test_get_category_male():
    """
    This function tests the get_category function for male athletes.
    GIVEN a male athlete's sex and year of birth
    WHEN the function is called
    THEN it returns the correct category.
    """
    current_year = NOW.year
    assert get_category("M", current_year - 20) == "A"
    assert get_category("M", current_year - 18) == "J"
    assert get_category("M", current_year - 16) == "R"
    assert get_category("M", current_year - 14) == "R"
    assert get_category("M", current_year - 12) == "EA"
    assert get_category("M", current_year - 10) == "EB"
    assert get_category("M", current_year - 9) == "EC"
    assert get_category("M", current_year - 8) == "G"
    assert get_category("M", current_year - 4) == "nan"


def test_get_category_female():
    """
    This function tests the get_category function for female athletes.
    GIVEN a female athlete's sex and year of birth
    WHEN the function is called
    THEN it returns the correct category.
    """
    current_year = NOW.year
    assert get_category("F", current_year - 20) == "A"
    assert get_category("F", current_year - 18) == "A"
    assert get_category("F", current_year - 16) == "J"
    assert get_category("F", current_year - 14) == "R"
    assert get_category("F", current_year - 12) == "EA"
    assert get_category("F", current_year - 9) == "EB"
    assert get_category("F", current_year - 8) == "EC"
    assert get_category("F", current_year - 7) == "G"
    assert get_category("F", current_year - 3) == "nan"


def test_shrink():
    """
    GIVEN: a dataframe
    WHEN: the shrink function is called
    THEN: it returns a dataframe with only valid rows (RaceStatus == T)
        and without rows with CalculationFlag == A
    """
    df = shrink(INPUT_DATASET)
    assert df["RaceStatus"].unique() == ["T"]
    assert "A" not in df["CalculationFlag"].unique()


def test_get_counts():
    """
    GIVEN: a dataframe
    WHEN: the get_counts function is called
    THEN: it returns a dataframe with the correct counts of athletes for each team
        both present and total.
    """
    df_counts = get_counts(INPUT_DATASET)
    assert df_counts["Presenti"].tolist() == [9, 9, 7]
    assert df_counts["Totali"].tolist() == [11, 10, 9]
    assert df_counts["Totali"].sum() == 30

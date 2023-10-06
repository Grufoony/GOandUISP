import pandas as pd
import numpy as np
from GOandUISP import converter

'''
This function tests the converter._split_names function.
GIVEN a full name
WHEN the function is called
THEN it returns a tuple containing the name and the surname.
'''


def test_split_names():
    assert converter._split_names('Rossi Mario') == ('MARIO', 'ROSSI')


'''
This function tests the converter.format function.
GIVEN a dataframe
WHEN the function is called
THEN it returns a dataframe with the correct column labels, the correct style names and the correct names format.
'''


def test_format():
    df = pd.read_excel('datasets/format_test.xlsx', header=None)
    out = converter.format(df)
    assert out.columns.tolist() == converter._in_columns
    assert (set(out.Style.unique())) == set(converter._styles.keys())
    assert out['Name'].tolist() == ['ROSSI MARIO', 'ROSSI MARIO',
                                    'ROSSI MARIO', 'ROSI MARIA', 'ROSI MARIA']
    assert set(out['Team'].tolist()) == set(['Aosta', 'Catanzaro'])


'''
This function tests the converter.format function in the relay case.
GIVEN a dataframe
WHEN the function is called
THEN it returns a dataframe with the correct column labels, the correct style names and the correct names format.
'''


def test_format_relay():
    df = pd.read_excel('datasets/format_relay_test.xlsx', header=None)
    out = converter.format(df)
    assert out.columns.tolist() == converter._in_columns_relayrace
    assert (set(out.Style.unique())) == set(converter._styles.keys())
    assert out['Name'].tolist() == ['ROSSI MARIO', 'ROSSI MARIO',
                                    'ROSSI MARIO', 'ROSI MARIA', 'ROSI MARIA']
    assert set(out['Team'].tolist()) == set(['Aosta', 'Catanzaro'])


'''
This function tests the converter.print_counts function.
GIVEN a dataframe
WHEN the function is called
THEN it prints how many athletes are in each team and the total (partecipating medals).
'''


def test_print_counts(capfd):
    df = pd.read_excel('datasets/print_counts_test.xlsx', header=None)
    out = converter.format(df)
    converter.print_counts(out)
    out, err = capfd.readouterr()
    assert out == 'Aosta        3\nCatanzaro    1\nName: Team, dtype: int64\nTOTALE ATLETI PARTECIPANTI: 4\n'


'''
This function tests the converter.groupdata function.
GIVEN a dataframe
WHEN the function is called
THEN it returns a dataframe with the correct format.
'''


def test_groupdata():
    df = pd.read_excel('datasets/format_test.xlsx', header=None)
    out = converter.format(df)
    out = converter.groupdata(out)
    assert out.columns.tolist() == ['Cognome', 'Nome', 'Anno', 'Sesso',
                                    'Gara1', 'Tempo1', 'Gara2', 'Tempo2', 'Gara3', 'Tempo3', 'Societa']
    assert out.loc[0].tolist() == ['ROSI', 'MARIA', 2011, ' F ',
                                   '100 M', ' 01\'26"90 ', np.nan, np.nan, np.nan, np.nan, 'Catanzaro']
    assert out.loc[1].tolist() == ['ROSSI', 'MARIO', 2013, ' M ',
                                   '50 Delfino', ' 00\'47"10 ', '100 Dorso', ' 01\'24"80 ', '200 Rana', ' 01\'24"80 ', 'Aosta']

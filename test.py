import pandas as pd
import pytest

from GOandUISP import converter

# def data():
#     # create a dataframe with the columns converter._in_columns
#     df = pd.DataFrame(columns = ['Maria Rosi', 2003, 'F', 'ITA', 200, 'R', 'Aosta', 1, 1, 1, '00:30:00', 1, 1, 1, 1, 1, 1, '00:30:00', 1, 1])
#     # add a row with data as indexed by the converter._in_columns
#     df.loc[0] = ['Mario Rossi', 2000, 'M', 'ITA', 50, 'S', 'Aosta', 1, 1, 1, '00:30:00', 1, 1, 1, 1, 1, 1, '00:30:00', 1, 1]
#     df.loc[1] = ['Mario Rossi', 2000, 'M', 'ITA', 100, 'D', 'Aosta', 1, 1, 1, '00:40:00', 1, 1, 1, 1, 1, 1, '00:40:00', 1, 1]
#     # df.loc[2] = ['Maria Rosi', 2003, 'F', 'ITA', 200, 'R', 'Aosta', 1, 1, 1, '00:30:00', 1, 1, 1, 1, 1, 1, '00:30:00', 1, 1]
#     return df

'''
This function tests the converter._split_names function.
GIVEN a full name
WHEN the function is called
THEN it returns a tuple containing the name and the surname.
'''
def test_split_names():
    assert converter._split_names('Mario Rossi') == ('ROSSI', 'MARIO')

# '''
# This function tests the converter.format function.
# GIVEN a dataframe
# WHEN the function is called
# THEN it returns a dataframe with the correct column labels, the correct style names and the correct names format.
# '''
# def test_format():
#     df = data()
#     df = converter.format(df)
#     assert df.columns.tolist() == converter._in_columns
#     assert df['Style'].tolist() == ['SL', 'Dorso', 'Rana']
#     assert df['Name'].tolist() == ['ROSSI', 'ROSSI', 'ROSI']
    
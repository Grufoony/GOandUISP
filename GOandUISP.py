import pandas as pd


class converter:
    __version__ = (1, 4, 1)
    # races dictionary: GoAndSwim -> dbMeeting
    _styles = {'F': 'Delfino', 'D': 'Dorso', 'R': 'Rana', 'S': 'SL', 'M': 'M'}
    _in_columns = ['Name', 'Year', 'Sex', '', 'Distance', 'Style', 'Team'] + \
        [''] * 3 + ['Time'] + [''] * 2 + ['Boolean', 'Absent'] + [''] * 5
    _in_columns_relayrace = ['Name', 'Year', 'Sex', '', 'Distance', 'Team', 'Style'] + \
        [''] * 3 + ['Time'] + [''] * 2 + ['Boolean', 'Absent'] + [''] * 5

    '''
    This function splits a full name into name and surname.
    If the full name is composed by more than two words, it asks the user to insert the surname.
    
    Parameters
    ----------
    full_name : str
        The full name to be splitted.

    Returns
    -------
    tuple
        A tuple containing the name and the surname.
    '''
    @staticmethod
    def _split_names(full_name: str) -> tuple:
        if len(full_name.split()) > 2:
            print("Inserisci i dati di " + str(full_name) + ": ")
            while True:
                surname = input("Inserisci il COGNOME: ").upper()
                if surname in full_name.upper():
                    name = full_name.upper().replace(surname + ' ', '')
                    break
                else:
                    print("COGNOME non presente nel nome, riprova: ")
            return name, surname
        else:
            name_column = full_name.split()
            return name_column[1].upper(), name_column[0].upper()

    '''
    This function is the main function of the class. It takes a file name as input and returns a pandas dataframe.
    The output dataset has the correct column labels, the correct style names and the correct names format.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe to be converted.

    Returns
    -------
    pandas.core.frame.DataFrame
        The converted dataframe.
    '''
    @classmethod
    def format(cls, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        # drop staffette rows
        df = df.drop(
            df[df[2] == 0].index).reset_index(drop=True)
        # drop nomiStaffette column, if exists
        if len(df.columns) == 21:
            df.drop(df.columns[1], axis=1, inplace=True)

        df.columns = cls._in_columns
        # check if style column is correct
        incorrect_styles = False
        for style in df.Style.unique():
            if style.split()[0] not in list(cls._styles.keys()):
                incorrect_styles = True
                break

        if incorrect_styles:
            df.columns = cls._in_columns_relayrace

        df['Name'] = df['Name'].str.strip()
        df['Name'] = df['Name'].str.replace('  ', ' ')

        return df

    '''
    This function prints how many athletes are in each team and the total (partecipating medals).

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe with the data to be counted.

    Returns
    -------
    None
    '''
    @classmethod
    def print_counts(cls, df: pd.core.frame.DataFrame) -> None:
        # now print how many athletes are in each team and the total (partecipating medals)
        counter_df = df.drop(
            df.loc[df['Absent'].str.strip() == 'A'].index, inplace=False)
        counter_df = counter_df.groupby(['Name', 'Year', 'Sex', 'Team'])[
            ['Time']].agg(list)

        print(counter_df.index.get_level_values('Team').value_counts())
        print("TOTALE ATLETI PARTECIPANTI: " + str(len(counter_df.index)))

    '''
    This function takes a dataframe as input and returns a new dataframe with the correct format.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        The dataframe to be converted.

    Returns
    -------
    pandas.core.frame.DataFrame
        The converted dataframe.
    '''
    @classmethod
    def groupdata(cls, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        # keep only rows with boolean set to T (valid times) and strip spaces in style column
        df.drop(
            df.loc[df['Boolean'].str.strip() != 'T'].index, inplace=True)
        df['Style'] = df['Style'].str.strip()
        # keeping only interesting data
        df = df[['Name', 'Year', 'Sex',
                 'Style', 'Distance', 'Time', 'Team']]
        # replacing style names
        df = df.replace({'Style': cls._styles})
        df['Race'] = df['Distance'].astype(
            str) + " " + df['Style']
        # groupby races and times, i.e. get unique athletes
        df = df.groupby(['Name', 'Year', 'Sex', 'Team'])[
            ['Race', 'Time']].agg(list)

        # creates empty output database with columns' names
        out_columns = ['Cognome', 'Nome', 'Anno', 'Sesso']
        max_len = df['Race'].apply(len).max()
        for i in range(max_len):
            out_columns.append('Gara' + str(i+1))
            out_columns.append('Tempo' + str(i+1))
        out_columns.append('Societa')
        out_df = pd.DataFrame(columns=out_columns)

        out_df['Anno'] = df.index.get_level_values('Year')
        out_df['Sesso'] = df.index.get_level_values('Sex')
        out_df['Societa'] = df.index.get_level_values('Team')

        # get unique athletes
        athletes = df.index

        # split name column into words and ask surname in input if the number of words is greater than 2
        for index, full_name in enumerate(athletes.get_level_values('Name')):
            name, surname = cls._split_names(full_name=full_name)
            out_df.loc[index, 'Nome'] = name
            out_df.loc[index, 'Cognome'] = surname

        for index, race, time in zip(range(len(df['Race'])), df['Race'], df['Time']):
            for i in range(len(race)):
                out_df.loc[index, 'Gara' + str(i+1)] = race[i]
                out_df.loc[index, 'Tempo' + str(i+1)] = time[i]

        return out_df

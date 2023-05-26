import pandas as pd
import os
__version__ = "1.3.7"
# races dictionary: GoAndSwim -> dbMeeting
_styles = {'F': 'Delfino', 'D': 'Dorso', 'R': 'Rana', 'S': 'SL', 'M': 'M'}
_in_columns = ['Name', 'Year', 'Sex', '', 'Distance', 'Style', 'Team'] + \
    [''] * 3 + ['Time'] + [''] * 2 + ['Boolean', 'Absent'] + [''] * 5


def convert(file_name):
    input_file = pd.read_excel(file_name, header=None)
    # drop staffette rows
    input_file = input_file.drop(
        input_file[input_file[2] == 0].index).reset_index(drop=True)
    # drop nomiStaffette column, if exists
    if len(input_file.columns) == 21:
        input_file.drop(input_file.columns[1], axis=1, inplace=True)

    input_file.columns = _in_columns
    # check if style column is correct
    incorrect_styles = False
    for style in input_file.Style.unique():
        if style not in list(_styles.keys()):
            incorrect_styles = True
            break

    if incorrect_styles:
        new_cols = ['Name', 'Year', 'Sex', '', 'Distance', 'Team', 'Style'] + \
            [''] * 3 + ['Time'] + [''] * 2 + ['Boolean', 'Absent'] + [''] * 5
        input_file.columns = new_cols

    # correctly format names
    input_file['Name'] = input_file['Name'].str.strip()
    input_file['Name'] = input_file['Name'].str.replace('  ', ' ')
    print(input_file.head())

    # now print how many athletes are in each team and the total (partecipating medals)
    counter_df = input_file.drop(
        input_file.loc[input_file['Absent'].str.strip() == 'A'].index, inplace=False)
    counter_df = counter_df.groupby(['Name', 'Year', 'Sex', 'Team'])[
        ['Time']].agg(list)

    print(counter_df.index.get_level_values('Team').value_counts())
    print("TOTALE ATLETI PARTECIPANTI: " + str(len(counter_df.index)))

    input("Premere un tasto qualsiasi per continuare...")

    # keep only rows with boolean set to T (valid times) and strip spaces in style column
    input_file.drop(
        input_file.loc[input_file['Boolean'].str.strip() != 'T'].index, inplace=True)
    input_file['Style'] = input_file['Style'].str.strip()
    # keeping only interesting data
    input_file = input_file[['Name', 'Year', 'Sex',
                             'Style', 'Distance', 'Time', 'Team']]
    # replacing style names
    input_file = input_file.replace({'Style': _styles})
    input_file['Race'] = input_file['Distance'].astype(
        str) + " " + input_file['Style']
    # groupby races and times, i.e. get unique athletes
    input_file = input_file.groupby(['Name', 'Year', 'Sex', 'Team'])[
        ['Race', 'Time']].agg(list)

    # creates empty output database with columns' names
    out_columns = ['Cognome', 'Nome', 'Anno', 'Sesso']
    max_len = input_file['Race'].apply(len).max()
    for i in range(max_len):
        out_columns.append('Gara' + str(i+1))
        out_columns.append('Tempo' + str(i+1))
    out_columns.append('Societa')
    output_file = pd.DataFrame(columns=out_columns)

    output_file['Anno'] = input_file.index.get_level_values('Year')
    output_file['Sesso'] = input_file.index.get_level_values('Sex')
    output_file['Societa'] = input_file.index.get_level_values('Team')

    # get unique athletes
    athletes = input_file.index

    # split name column into words and ask surname in input if the number of words is greater than 2
    for index, full_name in enumerate(athletes.get_level_values('Name')):
        if len(full_name.split()) > 2:
            print("Inserisci i dati di " + str(athletes[index]) + ": ")
            while True:
                surname = input("Inserisci il COGNOME: ").upper()
                if surname in full_name.upper():
                    name = full_name.upper().replace(surname + ' ', '')
                    break
                else:
                    print("COGNOME non presente nel nome, riprova: ")
            output_file.loc[index, 'Nome'] = name
            output_file.loc[index, 'Cognome'] = surname
        else:
            name_column = full_name.split()
            output_file.loc[index, 'Nome'] = name_column[1].upper()
            output_file.loc[index, 'Cognome'] = name_column[0].upper()

    for index, race, time in zip(range(len(input_file['Race'])), input_file['Race'], input_file['Time']):
        for i in range(len(race)):
            output_file.loc[index, 'Gara' + str(i+1)] = race[i]
            output_file.loc[index, 'Tempo' + str(i+1)] = time[i]

    # print output_file on xlsx file
    output_file.to_excel(os.path.splitext(file_name)[0] + '.xlsx', index=False)


if __name__ == "__main__":
    print("GOandUISP v" + __version__ + " by Gregorio Berselli.")
    print("Per informazioni su come utilizzare il programma si consulti la repository GitHub: https://github.com/Grufoony/GOandUISP\n\n")
    for f in os.listdir():
        if f.endswith(".xlsx") or f.endswith(".xls"):
            convert(f)
            if not f.endswith(".xlsx"):
                os.remove(f)
            print("File " + f + " convertito con successo!")
    print("Tutti i file presenti nella cartella sono stati convertiti con successo!")

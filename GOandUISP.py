import pandas as pd
# races dictionary: GoAndSwim -> dbMeeting
styles = { 'F':'Delfino', 'D':'Dorso', 'R':'Rana', 'S':'SL'}
in_columns = ['Name', 'Year', 'Sex', '', 'Distance', 'Style', 'Team'] + [''] * 3 + ['Time'] + [''] * 2 + ['Boolean'] + [''] * 6
input_file = pd.read_excel("input.xlsx")
input_file.columns=in_columns
# keep only rows with boolean set to T (valid times) and strip spaces in style column
input_file.drop(input_file.loc[input_file['Boolean'].str.strip() != 'T'].index, inplace=True)
input_file['Style'] = input_file['Style'].str.strip()
#keeping only interesting data
input_file = input_file[['Name', 'Year', 'Sex', 'Style', 'Distance', 'Time', 'Team']]
# replacing style names
input_file = input_file.replace({'Style': styles})
input_file['Race'] = input_file['Distance'].astype(str) + " " + input_file['Style']
# groupby races and times, i.e. get unique athletes
input_file = input_file.groupby(['Name', 'Year', 'Sex', 'Team'])[['Race', 'Time']].agg(list)

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

# split name column into words and ask name/surname by input if number of words is greater than 2
for index, full_name in zip(range(len(athletes)), athletes.get_level_values('Name')):
    if len(full_name.split()) > 2:
        print("Inserisci i dati di " + str(athletes[index]) + ": ")
        surname = input("Inserisci il cognome: ")
        name = input("Inserisci il nome: ")
        output_file.loc[index, 'Nome'] = name.upper()
        output_file.loc[index, 'Cognome'] = surname.upper()
    else:
        name_column = full_name.split()
        output_file.loc[index, 'Nome'] = name_column[1].upper()
        output_file.loc[index, 'Cognome'] = name_column[0].upper()

for index, race, time in zip(range(len(input_file['Race'])), input_file['Race'] , input_file['Time']):
    for i in range(len(race)):
        output_file.loc[index, 'Gara' + str(i+1)] = race[i]
        output_file.loc[index, 'Tempo' + str(i+1)] = time[i]

# print output_file on xlsx file
output_file.to_excel("output.xlsx", index=False)
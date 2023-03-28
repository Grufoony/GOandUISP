import pandas as pd
# races dictionary: GoAndSwim -> dbMeeting
styles = { 'F':'Delfino', 'D':'Dorso', 'R':'Rana', 'S':'SL'}
in_columns = ['Name', 'Year', 'Sex', '', 'Distance', 'Style', 'Team'] + [''] * 3 + ['Time'] + [''] * 2 + ['Boolean'] + [''] * 6
input = pd.read_excel("input.xlsx")
input.columns=in_columns
# keep only rows with boolean set to T (valid times) and strip spaces in style column
input.drop(input.loc[input['Boolean'].str.strip() != 'T'].index, inplace=True)
input['Style'] = input['Style'].str.strip()
#keeping only interesting data
input = input[['Name', 'Year', 'Sex', 'Style', 'Distance', 'Time', 'Team']]
# replacing style names
input = input.replace({'Style': styles})
input['Race'] = input['Distance'].astype(str) + " " + input['Style']
# groupby races and times
input = input.groupby(['Name', 'Year', 'Sex', 'Team'])[['Race', 'Time']].agg(list)

out_columns = ['Cognome', 'Nome', 'Anno', 'Sesso']
output = pd.DataFrame(columns=out_columns)

max_len = input['Race'].apply(len).max()
for i in range(max_len):
    out_columns.append('Gara' + str(i+1))
    out_columns.append('Tempo' + str(i+1))
out_columns.append('Societa')

# split name column into name and surname keeping only the first two words
name_column = input.index.get_level_values('Name')
name_column = name_column.str.split(expand=True, n=2)
output['Nome'] = name_column.get_level_values(1)
output['Cognome'] = name_column.get_level_values(0)

output['Anno'] = input.index.get_level_values('Year')
output['Sesso'] = input.index.get_level_values('Sex')

for index, race, time in zip(range(len(input['Race'])), input['Race'] , input['Time']):
    for i in range(len(race)):
        output.loc[index, 'Gara' + str(i+1)] = race[i]
        output.loc[index, 'Tempo' + str(i+1)] = time[i]

output['Societa'] = input.index.get_level_values('Team')
# print output on xlsx file
output.to_excel("output.xlsx", index=False)
import pandas as pd
# races dictionary: GoAndSwim -> dbMeeting
styles = { ' F ':'Delfino', ' D ':'Dorso', ' R ':'Rana', ' S ':'SL'}

input = pd.read_excel("input.xlsx")
# keep only rows with boolean set to T (valid times)
input.drop(input.loc[input['Boolean'] != ' T '].index, inplace=True)
#keeping only interesting data
input = input[['Name', 'Year', 'Sex', 'Style', 'Distance', 'Time', 'Team']]
# replacing style names
input = input.replace({'Style': styles})
input['Race'] = input['Distance'].astype(str) + " " + input['Style']
# groupby races and times
input = input.groupby(['Name', 'Year', 'Sex', 'Team'])[['Race', 'Time']].agg(list)

out_columns = ['Cognome', 'Nome', 'Anno', 'Sesso']

max_len = input['Race'].apply(len).max()
for i in range(max_len):
    out_columns.append('Gara' + str(i+1))
    out_columns.append('Tempo' + str(i+1))
out_columns.append('Societa')

output = pd.DataFrame(columns=out_columns)

# split name column into name and surname keeping only the first two words
name_column = input.index.get_level_values('Name')
name_column = name_column.str.split(expand=True, n=2)
output['Nome'] = name_column.get_level_values(1)
output['Cognome'] = name_column.get_level_values(0)

output['Anno'] = input.index.get_level_values('Year')
output['Sesso'] = input.index.get_level_values('Sex')
output['Societa'] = input.index.get_level_values('Team')

for index, race, time in zip(range(len(input['Race'])), input['Race'] , input['Time']):
    for i in range(len(race)):
        output.loc[index, 'Gara' + str(i+1)] = race[i]
        output.loc[index, 'Tempo' + str(i+1)] = time[i]

# print output on xlsx file
output.to_excel("output.xlsx", index=False)
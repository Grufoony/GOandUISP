import pandas as pd

# read the excel file
df = pd.read_excel('finalisti.xls')

# create a df with the columns CodSocieta Cognome Nome Anno Sesso Gara Tempo Societa Regione
out = pd.DataFrame(columns=['CodSocieta', 'Cognome', 'Nome', 'Anno', 'Sesso', 'Gara', 'Tempo', 'Societa', 'Regione'])

out["CodSocieta"] = df["CodFisSocieta"]
out["Societa"] = df["Società"]
# regione = EMilia Romagna for all
out["Regione"] = "Emilia-Romagna"
out["Gara"] = "100 misti"
out["Tempo"] = df["Tempo"]
out["Sesso"] = df["Sesso"]
out["Anno"] = df["Anno"]

import src.go_and_uisp as util
# cycle over atleta column taking also the index
for index, atleta in df["Atleta"].items():
    name, surname = util.split_names(atleta)
    out.at[index, "Nome"] = name
    out.at[index, "Cognome"] = surname

#save csv
out.to_csv('uffa.csv', index=False, sep=';')
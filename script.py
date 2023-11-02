import os
import pandas as pd

CATEGORY_PRIORITIES = {
    "EC": 1,
    "EA1": 2,
    "EA2": 3,
    "EB1": 4,
    "EB2": 5,
    "R": 6,
    "J": 7,
    "A": 8,
}


def get_category(sex: str, year: int) -> str:
    """
    This function returns the category given sex and year.
    """
    if sex == "m":
        if year < 2006:
            return "A"
        if year < 2008:
            return "J"
        if year < 2011:
            return "R"
        else:
            return "nan"
    else:
        if year < 2008:
            return "A"
        if year < 2010:
            return "J"
        if year < 2012:
            return "R"


for file in os.listdir():
    if "-staffette" in file:
        df_staffette = pd.read_csv(file, sep=";")
        df_data = pd.read_csv(file.replace("-staffette", ""), sep=";")

# drop last two cols
df_staffette = df_staffette.drop(df_staffette.columns[-2:], axis=1)

# glue together 'Cognome' and 'Nome' of df_data
df_data["Nome"] = df_data["Cognome"] + " " + df_data["Nome"]
# make 'Nome' column lowercase
df_data["Nome"] = df_data["Nome"].str.lower()
df_data["Nome"] = df_data["Nome"].str.strip()

col_names = [
    "Codice",
    "Societa",
    "Categoria",
    "Sesso",
    "Gara",
    "Tempo",
    "A0",
    "A1",
    "A2",
    "A3",
]
df_staffette.columns = col_names

# add a column 'CategoriaVera' to df_staffette
df_staffette["CategoriaVera"] = ""

for row in df_staffette.itertuples():
    categories = []
    for i in range(4):
        col = f"A{i}"
        athlete = getattr(row, col)
        if str(athlete) == "nan":
            continue
        athlete = athlete.lower()
        athlete = athlete.strip()
        # seach for athlete in df_data with the same CodSocieta
        societa = df_data.loc[df_data["CodSocietà"] == row.Codice]
        search = societa.loc[df_data["Nome"] == athlete]
        # if search is empty continue
        if search.empty:
            continue
        sex = search["Sesso"].values[0]
        year = search["Anno"].values[0]
        sex.lower().strip()
        # sex.strip()
        category = get_category(sex, year)
        categories.append(category)

    # take the max category given CATEGORIES dict
    if len(categories) == 0:
        category = "nan"
    else:
        category = max(categories, key=lambda x: CATEGORY_PRIORITIES[x])

    df_staffette.at[row.Index, "CategoriaVera"] = category

# save df_staffette to csv
df_staffette.to_csv("test.csv", index=False, sep=";")

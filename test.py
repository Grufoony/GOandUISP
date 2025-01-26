from goanduisp.core import groupdata, get_counts
import pandas as pd
from goanduisp.io import print_counts

df = pd.read_csv("prova.csv", sep=";")
# print(df)
# df = shrink(df)
# print(df)
# groupdata(df, by_points=True, use_jolly=True)
print_counts(df)

"""
Questo programma è stato creato per la manifestazione "YOUNG CHALLENGE".
"""

from goanduisp.core import accumulate
from goanduisp.io import info

__version__ = "15/04/2024"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(info(__author__, __version__))
    print(__doc__)
    # ask for jolly count
    use_jolly = input("Vuoi considerare i jolly? [s/n] ").lower()
    accumulate(points=True, jolly=use_jolly.strip() == "s")
    changed_files = []
    for f in os.listdir():
        if (f.endswith(".xlsx") or f.endswith(".xls")) and not "ACCUMULO" in f:
            df = pd.read_excel(f, header=None)
            # check if the file has 20 or 21 columns
            if len(df.columns) < 20 or len(df.columns) > 21:
                print(
                    "Il file "
                    + f
                    + " non è formattato correttamente per l'accumulo e verrà saltato."
                )
                continue
            df = reformat(df=df)
            if counts:
                print_counts(df=df)
                input("Premi INVIO per continuare...")
            out = groupdata(df=df)
            out.to_excel(f"ACCUMULATO_{f}", index=False)
            if points:
                out2 = groupdata(df=df, by_points=points, use_jolly=jolly, out_df=out)
                out2.to_excel(
                    f'ACCUMULO_{f.replace(".xlsx", "")}_PUNTEGGI.xlsx', index=True
                )
            changed_files.append(f)
    if len(changed_files) == 0:
        print("Non ci sono file da accumulare nella cartella corrente.")
    else:
        print("I file accumulati sono: ")
        for f in changed_files:
            print(f)

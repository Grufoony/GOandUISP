import tkinter as tk
from tkinter import messagebox, filedialog
import pathlib
from goanduisp.core import *
from goanduisp.io import import_df

__version__ = "2025.2.24"
__author__ = "Gregorio Berselli"


def point_formula(point: int, jolly: int) -> int:
    return point * jolly if jolly > 0 else point


def rank_teams_gui():
    file_path = filedialog.askopenfilename(
        title="Seleziona il file contenente i risultati"
    )
    if not file_path:
        return

    df = import_df(file_path)
    df = shrink(df)

    use_jolly = messagebox.askyesno("Jolly", "Vuoi considerare i jolly?")
    try:
        if use_jolly:
            df = rank_teams(df, point_formula=point_formula)
        else:
            df = rank_teams(df)
    except Exception as e:
        messagebox.showerror(
            "Errore", f"Errore durante il calcolo della classifica: {e}"
        )
        return

    file_name = f"team_ranking{'_jolly' if use_jolly else ''}.csv"
    df.to_csv(file_name, index=True, sep=";")
    messagebox.showinfo("Successo", f"Classifica squadre salvata in '{file_name}'")


def counts():
    file_path = filedialog.askopenfilename(
        title="Seleziona il file contenente i risultati"
    )
    if not file_path:
        return

    df = import_df(file_path)
    try:
        df = get_counts(df)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il calcolo dei conteggi: {e}")
        return

    file_name = "conteggi.csv"
    df.to_csv(file_name, index=True, sep=";")
    messagebox.showinfo("Successo", f"Conteggi salvati in '{file_name}'")


def categorie_staffette():
    relay_file_path = filedialog.askopenfilename(
        title="Selezionare il file (portale) delle iscrizioni delle staffette."
    )
    if not relay_file_path:
        return
    individual_file_path = filedialog.askopenfilename(
        title="Selezionare il file (portale) delle iscrizioni individuali."
    )
    if not individual_file_path:
        return

    df_relay = import_df(relay_file_path)
    df_individual = import_df(individual_file_path)

    try:
        df_relay, missing_athletes = fill_categories(df_relay, df_individual)
        if missing_athletes:
            messagebox.showwarning(
                "Atleti mancanti",
                f"Non sono state trovate le seguenti iscrizioni individuali:\n{"\n".join([f"\n{team}:\n  " + "\n  ".join(athletes) for team, athletes in missing_athletes.items()])}",
            )
    except Exception as e:
        messagebox.showerror(
            "Errore", f"Errore durante il calcolo delle categorie: {e}"
        )
        return

    file_name = "iscrizioni-staffette.csv"
    df_relay.to_csv(file_name, index=False, sep=";")
    messagebox.showinfo("Successo", f"Iscrizioni staffette salvate in '{file_name}'")


def top100():
    file_path = filedialog.askopenfilename(
        title="Seleziona il file contenente i risultati"
    )
    if not file_path:
        return

    df = import_df(file_path)
    df = shrink(df)

    use_jolly = messagebox.askyesno("Jolly", "Vuoi considerare i jolly?")
    try:
        df = groupdata(df, by_points=True, use_jolly=use_jolly)
    except Exception as e:
        messagebox.showerror(
            "Errore", f"Errore durante il calcolo della classifica: {e}"
        )
        return

    file_name = "top100.csv"
    df.to_csv(file_name, index=True, sep=";")
    messagebox.showinfo("Successo", f"Classifica squadre salvata in '{file_name}'")


def sono_pronto():
    file_path = filedialog.askopenfilename(
        title="Seleziona il file contenente i risultati"
    )
    if not file_path:
        return

    df = import_df(file_path)
    df = shrink(df=df, keep_valid_times=True)
    dir_path = filedialog.askdirectory(
        title="Seleziona la cartella contenente le tabelle tempi/punteggi"
    )
    try:
        df = assign_points_by_time(df, dir_path)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante l'assegnazione dei punti: {e}")
        return

    file_name = "points.csv"
    df.to_csv(file_name, index=False, header=True, sep=";")
    messagebox.showinfo("Successo", f"File punteggi salvato in '{file_name}'")


def combinata():
    dir_path = filedialog.askdirectory(
        title="Seleziona la cartella contenente i risultati della combinata"
    )
    if not dir_path:
        return
    # Concat all dataframes in the directory
    df = pd.DataFrame()
    for file_path in pathlib.Path(dir_path).iterdir():
        if file_path.suffix == ".csv":
            temp_df = import_df(file_path.as_posix())
            df = pd.concat([df, temp_df], ignore_index=True)
    try:
        df = groupdata(df, filterRace=" C")
        # Check if only one col name contains "Gara"
        if len([col for col in df.columns if "Gara" in col]) == 1:
            df["Gara1"] = "100 M"
            df.insert(0, "CodSocieta", "")
            df["Regione"] = ""
            file_name = "iscrizioni-combinata"
        else:
            df = df[df["GareDisputate"] >= 5]
            file_name = "accumulo"
    except Exception as e:
        messagebox.showerror(
            "Errore", f"Errore durante il calcolo della combinata: {e}"
        )
        return
    df.to_csv(f"{file_name}.csv", index=False, sep=";")
    messagebox.showinfo(
        "Successo", f"Classifica combinata salvata in '{file_name}.csv'"
    )


if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"Go And UISP - App - v{__version__}@BETA")

    frame = tk.Frame(root)
    frame.pack(expand=True)

    btn_counts = tk.Button(
        frame, text="Conteggi", command=counts, font=("Arial", 12), width=20, height=2
    )
    btn_counts.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

    btn_rank = tk.Button(
        frame,
        text="Classifica Squadre",
        command=rank_teams_gui,
        font=("Arial", 12),
        width=20,
        height=2,
    )
    btn_rank.grid(row=1, column=0, padx=20, pady=20)

    btn_categorie_staffette = tk.Button(
        frame,
        text="Assegna Categorie Staffette",
        command=categorie_staffette,
        font=("Arial", 12),
        width=20,
        height=2,
    )
    btn_categorie_staffette.grid(row=1, column=1, padx=20, pady=20)

    # Horizontal line with text
    label_yc = tk.Label(frame, text="Circuito YOUNG CHALLENGE", font=("Arial", 12))
    label_yc.grid(row=2, column=0, sticky="w", padx=20)

    separator = tk.Frame(frame, height=2, width=250, bg="black")
    separator.grid(row=2, column=1, pady=10)

    btn_top100 = tk.Button(
        frame,
        text="Classifica TOP 100",
        command=top100,
        font=("Arial", 12),
        width=20,
        height=2,
    )
    btn_top100.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    # Horizontal line with text
    label_circuito = tk.Label(frame, text="Circuito SONO PRONTO", font=("Arial", 12))
    label_circuito.grid(row=4, column=0, sticky="w", padx=20)

    separator = tk.Frame(frame, height=2, width=250, bg="black")
    separator.grid(row=4, column=1, pady=10)

    # SONO PRONTO button
    btn_sono_pronto = tk.Button(
        frame,
        text="Calcolo Punteggi Individuali",
        command=sono_pronto,
        font=("Arial", 12),
        width=25,
        height=2,
    )
    btn_sono_pronto.grid(row=5, column=0, columnspan=2, padx=20, pady=20)

    # Horizontal line with text
    label_circuito = tk.Label(frame, text="Combinata degli Stili", font=("Arial", 12))
    label_circuito.grid(row=6, column=0, sticky="w", padx=20)

    separator = tk.Frame(frame, height=2, width=250, bg="black")
    separator.grid(row=6, column=1, pady=10)

    # Combinata button
    btn_combinata = tk.Button(
        frame,
        text="Crea iscrizioni finali",
        command=combinata,
        font=("Arial", 12),
        width=25,
        height=2,
    )
    btn_combinata.grid(row=7, column=0, columnspan=2, padx=20, pady=20)

    root.mainloop()

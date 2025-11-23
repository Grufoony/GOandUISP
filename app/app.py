import tkinter as tk
from tkinter import messagebox, filedialog
import pathlib
import re

import pandas as pd
import polars as pl

from goanduisp.core import (
    compute_prices_individual,
    shrink,
    rank_teams,
    groupdata,
    fill_categories,
    assign_points_by_time,
    get_counts,
    time_to_int,
    int_to_time,
)
from goanduisp.io import import_df

__version__ = "2025.2.24"
__author__ = "Gregorio Berselli"


def point_formula(point: int, jolly: int) -> int:
    return point * jolly if jolly > 0 else point


def get_price_per_race_dialog():
    """
    Opens a dialog to configure prices per number of races.
    Returns a dictionary {num_races: price} or None if cancelled.
    """
    # Create a dialog to input prices per race
    price_dialog = tk.Toplevel()
    price_dialog.title("Configurazione Prezzi")
    price_dialog.geometry("400x450")

    tk.Label(
        price_dialog, text="Inserisci i prezzi per numero di gare:", font=("Arial", 12)
    ).pack(pady=10)

    # Container frame for canvas and scrollbar
    container = tk.Frame(price_dialog)
    container.pack(fill="both", expand=True, padx=10, pady=5)

    # Frame for price entries with scrollbar
    canvas = tk.Canvas(container, height=200)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    entries_frame = tk.Frame(canvas)

    entries_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=entries_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    price_entries = {}
    num_entries = [
        3
    ]  # Start with 3 entries, wrapped in list to allow modification in nested function

    def add_entry(num_races):
        row_frame = tk.Frame(entries_frame)
        row_frame.pack(pady=5)
        tk.Label(row_frame, text=f"{num_races} gara/e:", width=10).pack(side=tk.LEFT)
        entry = tk.Entry(row_frame, width=10)
        entry.insert(0, "0")  # Default values
        entry.pack(side=tk.LEFT)
        price_entries[num_races] = entry

    # Initialize with 3 entries
    for i in range(1, 4):
        add_entry(i)

    def add_more_entries():
        num_entries[0] += 1
        add_entry(num_entries[0])

    price_per_race = {}

    def confirm_prices():
        nonlocal price_per_race
        try:
            for num_races, entry in price_entries.items():
                price_per_race[num_races] = float(entry.get())
            price_dialog.destroy()
        except ValueError:
            messagebox.showerror(
                "Errore", "Inserisci valori numerici validi per i prezzi"
            )

    def cancel_prices():
        price_dialog.destroy()

    # Button to add more entries
    add_btn_frame = tk.Frame(price_dialog)
    add_btn_frame.pack(pady=10)
    tk.Button(
        add_btn_frame, text="Aggiungi altra fascia", command=add_more_entries, width=15
    ).pack()

    btn_frame = tk.Frame(price_dialog)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Conferma", command=confirm_prices, width=10).pack(
        side=tk.LEFT, padx=5
    )
    tk.Button(btn_frame, text="Annulla", command=cancel_prices, width=10).pack(
        side=tk.LEFT, padx=5
    )

    price_dialog.transient()
    price_dialog.grab_set()
    price_dialog.wait_window()

    return price_per_race if price_per_race else None


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
                f"Non sono state trovate le seguenti iscrizioni individuali:\n{'\n'.join([f'\n{team}:\n  ' + '\n  '.join(athletes) for team, athletes in missing_athletes.items()])}",
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
        df = df[df["GareDisputate"] >= 5]
        file_name = "accumulo"
        # Check that the time in TempoFiltro is 2* the time of other Tempoi columns
        for _, row in df.iterrows():
            # sum all the times with Tempo in the column name
            sum_time = sum(
                [
                    time_to_int(row[col])
                    for col in df.columns
                    if "Tempo" in col and "Filtro" not in col
                ]
            )
            # check if the sum is equal to the time in TempoFiltro
            if sum_time != time_to_int(row["TempoFiltro"]) * 2:
                print(
                    f"Errore: {row['Nome']} {row['Cognome']} {row['Societa']} {abs(sum_time - time_to_int(row['TempoFiltro']) * 2)}"
                )
                # Replace the time in TempoFiltro with the sum of the other times
                df.at[_, "TempoFiltro"] = int_to_time(
                    sum_time
                    - max(
                        [
                            time_to_int(row[col])
                            for col in df.columns
                            if "Tempo" in col and "Filtro" not in col
                        ]
                    )
                )
        df_subs = df.copy()
        # Set Gara1 as 100 M
        df_subs["Gara1"] = "100 M"
        df_subs["Tempo1"] = df_subs["TempoFiltro"]
        df_subs.insert(0, "CodSocieta", "")
        df_subs["Regione"] = ""
        # Keep only the columns needed
        df_subs = df_subs[
            [
                "CodSocieta",
                "Cognome",
                "Nome",
                "Anno",
                "Sesso",
                "Gara1",
                "Tempo1",
                "Societa",
                "Regione",
            ]
        ]

    except Exception as e:
        messagebox.showerror(
            "Errore", f"Errore durante il calcolo della combinata: {e}"
        )
        return
    df.to_csv("accumulo.csv", index=False, sep=";")
    df_subs.to_csv("iscrizioni-combinata.csv", index=False, sep=";")
    messagebox.showinfo(
        "Successo", f"Classifica combinata salvata in '{file_name}.csv'"
    )


def individual_prices():
    file_path = filedialog.askopenfilename(
        title="Seleziona il file contenente le iscrizioni individuali"
    )
    if not file_path:
        return

    # Extract the number in the file name
    match = re.search(r"\d+", file_path)
    if match:
        number = int(match.group())
    else:
        number = None

    df = import_df(file_path, engine="polars")
    # Assert that CodSocietà, Cognome, Nome, Anno, Sesso, Societa, Regione are in df columns
    assert all(
        col in df.columns
        for col in [
            "CodSocietà",
            "Cognome",
            "Nome",
            "Anno",
            "Sesso",
            "Societa",
            "Regione",
        ]
    ), "Missing required columns in dataframe"

    price_per_race = get_price_per_race_dialog()

    if not price_per_race:
        return

    try:
        df = compute_prices_individual(df, price_per_race)
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il calcolo dei prezzi: {e}")
        return
    file_name = (
        f"{number}-riepilogo-pagamenti-dettaglio-individuali.csv"
        if number is not None
        else "riepilogo-pagamenti-dettaglio-individuali.csv"
    )
    df.write_csv(file_name, separator=";")
    messagebox.showinfo("Successo", f"Riepilogo pagamenti salvato in '{file_name}'")


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

    # Horizontal line with text
    label_pagamenti = tk.Label(frame, text="Pagamenti", font=("Arial", 12))
    label_pagamenti.grid(row=8, column=0, sticky="w", padx=20)

    separator = tk.Frame(frame, height=2, width=250, bg="black")
    separator.grid(row=8, column=1, pady=10)

    # Individual prices button
    btn_individual_prices = tk.Button(
        frame,
        text="Calcolo costi individuali",
        command=individual_prices,
        font=("Arial", 12),
        width=25,
        height=2,
    )
    btn_individual_prices.grid(row=9, column=0, columnspan=2, padx=20, pady=20)

    root.mainloop()

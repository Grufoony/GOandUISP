import tkinter as tk
from tkinter import messagebox, filedialog
from goanduisp.core import *
from goanduisp.io import import_df

__version__ = "2025.2.16"
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


if __name__ == "__main__":
    root = tk.Tk()
    root.title(f"Go And UISP - App - v{__version__}@ALPHA")
    root.geometry("640x480")

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

    btn_top100 = tk.Button(
        frame,
        text="Classifica TOP 100",
        command=top100,
        font=("Arial", 12),
        width=20,
        height=2,
    )
    btn_top100.grid(row=1, column=1, padx=20, pady=20)

    root.mainloop()

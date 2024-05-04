import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import pandas as pd
import go_and_uisp as go


class DataFrameWindow(tk.Toplevel):  # Inherits from tk.Toplevel

    def __init__(
        self, your_dataframe, title, reset_index=True
    ):  # the dataframe you passed through is here
        super().__init__()

        # Frame for TreeView
        frame = tk.LabelFrame(self, text="DataFrame")
        frame.pack(fill="both", expand="true")
        frame.pack_propagate(0)

        # the size of the window.
        self.geometry("1280x720")
        # self.resizable(0, 0)
        self.title(title)  # the window title

        # This creates your Treeview widget.
        tv1 = ttk.Treeview(frame)
        tv1.place(
            relheight=1, relwidth=1
        )  # set the height and width of the widget to 100% of its container (frame).

        treescrolly = tk.Scrollbar(
            frame, orient="vertical", command=tv1.yview
        )  # command means update the yaxis view of the widget
        treescrollx = tk.Scrollbar(
            frame, orient="horizontal", command=tv1.xview
        )  # command means update the xaxis view of the widget
        tv1.configure(
            xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set
        )  # assign the scrollbars to the Treeview Widget
        treescrollx.pack(
            side="bottom", fill="x"
        )  # make the scrollbar fill the x axis of the Treeview widget
        treescrolly.pack(
            side="right", fill="y"
        )  # make the scrollbar fill the y axis of the Treeview widget

        if reset_index:
            your_dataframe.reset_index(inplace=True)
            your_dataframe.rename(columns={"index": "Indice"}, inplace=True)

        # this loads the dataframe into the treeview widget
        tv1["column"] = list(your_dataframe.columns)
        tv1["show"] = "headings"
        for column in tv1["columns"]:
            tv1.heading(column, text=column)  # let the column heading = column name

        df_rows = (
            your_dataframe.to_numpy().tolist()
        )  # turns the dataframe into a list of lists
        for row in df_rows:
            tv1.insert("", "end", values=row)  # inserts each list into the treeview.


class GUI:
    __version__ = (0, 1, 0)
    __author__ = "Grufoony"

    def __init__(self):
        self.cached_df = None
        self.file = ""

        self.main_win = tk.Tk()
        self.main_win.title("Swim Utils v" + ".".join(map(str, self.__version__)))
        self.main_win.minsize(width=500, height=300)

        self.menu_bar = tk.Menu(self.main_win)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        # add about menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.about_menu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About", "Go And Uisp v" + go.version()
            ),
        )
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        # add help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="Help", command=lambda: print("Help"))
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.main_win.config(menu=self.menu_bar)

        self.btn_print_counts = tk.Button(
            text="Print Counts", command=lambda: self.print_counts()
        )
        self.btn_print_counts.pack()

        self.btn_make_ranking = tk.Button(
            text="Make Ranking", command=lambda: self.make_ranking()
        )
        self.btn_make_ranking.pack()

        # self.relayButton = tk.Button(text="Staffetta", command=lambda : go.find_categories())
        # self.relayButton.pack()

    def __combobox(self, title: str, values: list):
        top = tk.Toplevel()  # use Toplevel() instead of Tk()
        tk.Label(top, text=title).pack()
        box_value = tk.StringVar()
        combo = ttk.Combobox(top, textvariable=box_value, values=values)
        combo.pack()
        combo.bind("<<ComboboxSelected>>", lambda _: top.destroy())
        top.grab_set()
        top.wait_window(top)  # wait for itself destroyed, so like a modal dialog
        return box_value.get()

    def open_file(self):
        while True:
            self.file = filedialog.askopenfilename()
            if type(self.file) == tuple:
                break
            try:
                if self.file.endswith(".csv"):
                    if "dbmeeting" in self.file:
                        df = pd.read_csv(self.file, sep=";")
                        self.cached_df = df
                    else:
                        df = pd.read_csv(self.file, sep=";", header=None)
                        self.cached_df = go.reformat(df)
                elif self.file.endswith(".xlsx"):
                    df = pd.read_excel(self.file, header=None)
                    self.cached_df = go.reformat(df)
                break
            except Exception as e:
                if self.file == "":
                    break
                messagebox.showerror("Invalid File", f"Error details: {e.__str__()}")

    def print_counts(self):
        if self.cached_df is None:
            messagebox.showerror("No File", "No file has been loaded yet.")
        # set filename as title
        DataFrameWindow(go.get_counts(self.cached_df), title=self.file)

    def make_ranking(self):
        if self.cached_df is None:
            messagebox.showerror("No File", "No file has been loaded yet.")
        result_df = go.groupdata(df=self.cached_df, split_names=False)
        # ask for jolly count and number of athletes to show
        use_jolly = messagebox.askyesno("Jolly", "Vuoi considerare i jolly?")
        # ask for playoff race making as choices the races in the dataframe
        columns = [
            f"Gara{i}" for i in range(1, int(result_df["GareDisputate"].max()) + 1)
        ]
        unique_races = (
            pd.concat([result_df[col] for col in columns]).dropna().unique().tolist()
        )
        # ask for playoff giving unique_races as choices
        playoff_race = self.__combobox(
            title="Seleziona la gara di spareggio", values=unique_races
        )
        show_first = simpledialog.askinteger(
            "Atleti da mostrare", "Quanti atleti per categoria vuoi mostrare?"
        )
        min_races = simpledialog.askinteger(
            "Gare minime",
            "Quante gare minime devono avere gli atleti per essere considerati?",
        )

        result_df = go.ranking(
            result_df,
            use_jolly=use_jolly,
            playoff_race=playoff_race,
            show_first=show_first,
            min_races=min_races,
        )
        DataFrameWindow(result_df, title=self.file)
        # except Exception as e:
        #     messagebox.showerror("Error", f"Error details: {e.__str__()}")


if __name__ == "__main__":
    gui = GUI()
    gui.main_win.mainloop()

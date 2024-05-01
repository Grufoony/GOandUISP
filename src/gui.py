import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import go_and_uisp as go


class DataFrameWindow(tk.Toplevel):  # Inherits from tk.Toplevel

    def __init__(
        self, your_dataframe, title
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

        # add also index
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
            tv1.insert(
                "", "end", values=row
            )  # inserts each list into the treeview.


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

        # self.combinedButton = tk.Button(text="Combinata", command=lambda : go.accumulate())
        # self.combinedButton.pack()

        # self.relayButton = tk.Button(text="Staffetta", command=lambda : go.find_categories())
        # self.relayButton.pack()

    def open_file(self):
        while True:
            self.file = filedialog.askopenfilename()
            if type(self.file) == tuple:
                break
            print(type(self.file))
            print(self.file)
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
                messagebox.showerror("Invalid File", f"Error details: {e.__context__}")

    def print_counts(self):
        if self.cached_df is None:
            messagebox.showerror("No File", "No file has been loaded yet.")
        # set filename as title
        DataFrameWindow(go.get_counts(self.cached_df), title=self.file)


if __name__ == "__main__":
    gui = GUI()
    gui.main_win.mainloop()

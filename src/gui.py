import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import go_and_uisp as go


class GUI:
    def __init__(self):
        self.mainWin = tk.Tk()
        self.mainWin.title("Go And Uisp v" + go.version())
        self.mainWin.minsize(width=500, height=300)

        self.menuBar = tk.Menu(self.mainWin)

        # File menu
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Exit", command=self.mainWin.quit)
        self.fileMenu.add_command(label="Open", command=self.openFile)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        # add about menu
        self.aboutMenu = tk.Menu(self.menuBar, tearoff=0)
        self.aboutMenu.add_command(label="About", command=lambda: print("About"))
        self.menuBar.add_cascade(label="About", menu=self.aboutMenu)
        # add help menu
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="Help", command=lambda: print("Help"))
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

        self.mainWin.config(menu=self.menuBar)

        # self.youngchallengeButton = tk.Button(text="Young Challenge", command=lambda : go.accumulate(points=True, jolly=True))
        # self.youngchallengeButton.pack()

        # self.combinedButton = tk.Button(text="Combinata", command=lambda : go.accumulate())
        # self.combinedButton.pack()

        # self.relayButton = tk.Button(text="Staffetta", command=lambda : go.find_categories())
        # self.relayButton.pack()

    def openFile(self):
        self.file = ""
        while True:
            self.file = filedialog.askopenfilename()
            if(type(self.file) == tuple):
                break
            print(type(self.file))
            print(self.file)
            try:
                df = pd.read_csv(self.file)
                self.cached_df = go.reformat(df)
                break
            except:
                if self.file == "":
                    break
                messagebox.showerror("Error", "Invalid file")


if __name__ == "__main__":
    gui = GUI()
    gui.mainWin.mainloop()

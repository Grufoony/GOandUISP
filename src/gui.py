import tkinter as tk
from tkinter import filedialog
import go_and_uisp as go

def openFile():
    # ask to open a file and return the path
    return filedialog.askopenfilename()


mainWin = tk.Tk()
mainWin.title("Go And Uisp v" + go.version())
mainWin.minsize(width=500, height=300)

menuBar = tk.Menu(mainWin)

# File menu
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label="Exit", command=mainWin.quit)
fileMenu.add_command(label="Open", command=openFile)
menuBar.add_cascade(label="File", menu=fileMenu)
# add about menu
aboutMenu = tk.Menu(menuBar, tearoff=0)
aboutMenu.add_command(label="About", command=print('About'))
menuBar.add_cascade(label="About", menu=aboutMenu)
# add help menu
helpMenu = tk.Menu(menuBar, tearoff=0)
helpMenu.add_command(label="Help", command=print("Help"))
menuBar.add_cascade(label="Help", menu=helpMenu)

mainWin.config(menu=menuBar)

youngchallengeButton = tk.Button(text="Young Challenge", command=go.accumulate(points=True, jolly=True))
youngchallengeButton.pack()

combinedButton = tk.Button(text="Combinata", command=go.accumulate())
combinedButton.pack()

relayButton = tk.Button(text="Staffetta", command=go.find_categories())
relayButton.pack()

# # Label
# my_label = tk.Label(text="I am a Label", font=("Arial", 24, "bold"))
# my_label.pack(side="left")

# # Button
# def button_clicked():
#     my_label.config(text="I got clicked")

# button = tk.Button(text="Click Me", command=button_clicked)
# button.pack()

# run
mainWin.mainloop()
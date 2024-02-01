import tkinter as tk
import go_and_uisp as go

window = tk.Tk()
window.title("Go And Uisp v" + go.version())
window.minsize(width=500, height=300)

youngchallengeButton = tk.Button(text="Young Challenge", command=go.accumulate(points=True, jolly=True))
youngchallengeButton.pack()

# # Label
# my_label = tk.Label(text="I am a Label", font=("Arial", 24, "bold"))
# my_label.pack(side="left")

# # Button
# def button_clicked():
#     my_label.config(text="I got clicked")

# button = tk.Button(text="Click Me", command=button_clicked)
# button.pack()

# run
window.mainloop()
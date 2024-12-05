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

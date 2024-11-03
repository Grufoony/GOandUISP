"""
This module contains the pipeline useful to convert files from a YOUNG CHALLENGE event.
"""

from goanduisp.core import accumulate
from goanduisp.version import __version_core__, __version_io__

__version__ = "15/04/2024"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"YOUNG CHALLENGE by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP: core v{__version_core__} - io v{__version_io__}\n")
    print('Questo programma è stato creato per la manifestazione "YOUNG CHALLENGE".\n')
    # ask for jolly count
    use_jolly = input("Vuoi considerare i jolly? [s/n] ").lower()
    accumulate(points=True, jolly=use_jolly.strip() == "s")

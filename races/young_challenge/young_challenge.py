"""
This module contains the pipeline useful to convert files from a YOUNG CHALLENGE event.
"""

import sys

sys.path.insert(1, ".")
# pylint: disable=wrong-import-position
from src import go_and_uisp as GOandUISP

# pylint: enable=wrong-import-position

__version__ = "08/11/2023"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"YOUNG CHALLENGE by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print('Questo programma è stato creato per la manifestazione "YOUNG CHALLENGE".\n')
    GOandUISP.accumulate(points=True, jolly=True)

"""
This module contains the pipeline useful to convert files from a COMBINATA STILI event.
"""

import sys

sys.path.insert(1, ".")
# pylint: disable=wrong-import-position
from src import go_and_uisp as GOandUISP

# pylint: enable=wrong-import-position

__version__ = "2023.11.08"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"COMBINATA STILI by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print('Questo programma è stato creato per la manifestazione "COMBINATA STILI".\n')
    GOandUISP.accumulate()

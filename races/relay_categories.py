"""
This module contains the pipeline useful to automatically add categories to a staffette file.
Requires the individual file to be present.
All files must be downloaded from the UISP nazionale portal.
"""

import sys

sys.path.insert(1, ".")
# pylint: disable=wrong-import-position
from src import go_and_uisp as GOandUISP

# pylint enable=wrong-import-position

__version__ = "05/12/2023"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"Relay Categories by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP v{GOandUISP.__version__}\n")
    print(
        "Questo programma riempie automaticamente la categoria nei file staffette,"
        + " se presente il file di iscrizioni individuali.\n"
    )
    GOandUISP.find_categories()

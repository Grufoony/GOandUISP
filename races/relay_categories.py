"""
This module contains the pipeline useful to automatically add categories to a staffette file.
Requires the individual file to be present.
All files must be downloaded from the UISP nazionale portal.
"""

from goanduisp.core import find_categories
from goanduisp.version import __version_core__, __version_io__

__version__ = "2023.12.5"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"Relay Categories by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP: core v{__version_core__} - io v{__version_io__}\n")
    print(
        "Questo programma riempie automaticamente la categoria nei file staffette,"
        + " se presente il file di iscrizioni individuali.\n"
    )
    find_categories()

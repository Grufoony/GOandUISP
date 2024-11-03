"""
This module contains the pipeline useful to convert files from a COMBINATA STILI event.
"""

from goanduisp.core import accumulate
from goanduisp.version import __version_core__, __version_io__

__version__ = "2023.11.08"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"COMBINATA STILI by {__author__}, aggiornato al {__version__}")
    print(f"Basato su GOandUISP: core v{__version_core__} - io v{__version_io__}\n")
    print('Questo programma è stato creato per la manifestazione "COMBINATA STILI".\n')
    accumulate()

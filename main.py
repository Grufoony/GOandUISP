from src import formatter as GOandUISP

__version__ = "2023.11.02"
__author__ = "Gregorio Berselli"

if __name__ == "__main__":
    print(f"GOandUISP v{__version__} by {__author__}\n")
    print(
        "Per informazioni su come utilizzare il programma si consulti il repository"
        " GitHub: https://github.com/Grufoony/GOandUISP\n\n"
    )
    GOandUISP.accumulate()
    GOandUISP.find_categories()

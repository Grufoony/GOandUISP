# Bologna Swimming League

Guida all'utilizzo dello script BSL.

## Creazione del file di input
Per iniziare, selezionare su Go And Swim le gare di interesse per andare a costruire le scquadre, per esempio i 50 Farfalla (è possibile anche selezionare tutte le gare, il filtro verrà inserito in seguito).
Una volta selezionate le gare, entrarvi dentro con il tasto a forma di foglio in basso a sinistra, premere la combinazione di tasti *CTRL+C* sul primo atleta per copiare i dati e incollare (*CTRL+V*) su un foglio Excel vuoto.
Salvare il file in formato *CSV - UTF8*.

## Utilizzo del programma
Una volta avviato il programma, selezionare il file precedentemente creato e inserire i parametri richiesti:
- Numero di squadre
- Seed: numero intero positivo. Serve per poter ricreare le stesse identiche squadre random in caso di necessità.
- Distanza
- Stile: codificato in *F, D, R, S, M*.
A questo punto il programma avrà prodotto il file *teams.csv* contenente le squadre.
Proseguendo nell'esecuzione, sarà inoltre possibile creare un file CSV per l'iscrizione alle gare individuali, fornendo come ulteriore input il riepilogo delle iscrizioni formato CSV ottenuto dal portale UISP, e l'iscrizione delle staffette.
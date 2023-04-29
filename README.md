# GOandUISP
Script Python per la conversione di file _.xlsx_ da output GoAndSwim a input per il portale online UISP.

## Guida rapida

### Ottenere l'eseguibile
Lo script si può eseguire sulla piattaforma [Google Colab](https://colab.research.google.com/github/Grufoony/GOandUISP/blob/main/GOandUISP.ipynb).

Per qualsiasi problema [scrivimi una mail](mailto:gregorio.berselli@studio.unibo.it).

### Preparare il file di input
1. Creare un file excel (_.xlsx_), e aprirlo con Excel. Questo file deve essere vuoto per il momento
2. Una volta aperto il file, aprire il file _.GAS_ della manifestazione che si vuole convertire
3. Selezionare le gare di interesse ed entrare in esse (tasto in basso a sinistra di GoAndSwim)
4. Senza dover fare nulla, si dovrebbe essere sul primo atleta dell'elenco. A questo punto eseguire la combinazione di tasti _CTRL + C_ (copia)
5. Andare nel file vuoto appena creato nella prima cella in alto a sinistra (la A1) ed eseguirle la combinazione di tasti _CTRL + V_ (incolla). In questo modo tutte le gare di interesse dovrebbero essere state copiate nel file Excel
6. Salvare il file e chiuderlo

Se è stato fatto tutto correttamente, basterà eseguire lo script _GOandUISP.py_ __nella stessa cartella__ del file: questo verrà sostituito con il file formattato correttamente.

__NOTA__: nel caso di atleti con più di un nome/cognome il programma chiederà di inserirli manualmente, comunicandovi tutti i dati che possiede di quel determinato atleta. Potete scrivere sia in maiuscolo che in minuscolo ed inserire spazi (per i nomi/cognomi multipli). Una volta inserito il nome/cognome multiplo richiesto, premere INVIO e ripetere l'azione ogni qualvolta richiesta dal programma. Al termine della procedura la finestra si chiuderà automaticamente.
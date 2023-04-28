# GOandUISP
Script Python per la conversione di file _.xlsx_ da output GoAndSwim a input per il portale online UISP.

## Guida rapida

### Ottenere l'eseguibile
Per utilizzare il programma è necessario ottenere l'eseguibile _GOandUISP.exe_: [scrivimi una mail](mailto:gregorio.berselli@studio.unibo.it).

Un'alternativa all'utilizzo dell'eseguibile (che a Windows di base non piace) è [Google Colab](https://colab.research.google.com/github/Grufoony/GOandUISP/blob/main/GOandUISP.ipynb)

### Preparare il file di input
1. Creare un file excel (_.xlsx_) chiamato _input_, e aprirlo con Excel. Questo file deve essere vuoto per il momento
2. Una volta aperto il file _input.xlsx_, aprire il file _.GAS_ della manifestazione che si vuole convertire
3. Selezionare le gare di interesse ed entrare in esse (tasto in basso a sinistra di GoAndSwim)
4. Senza dover fare nulla, si dovrebbe essere sul primo atleta dell'elenco. A questo punto eseguire la combinazione di tasti _CTRL + C_ (copia)
5. Andare nel file vuoto _input.xlsx_ nella prima cella in alto a sinistra (la A1) ed eseguirle la combinazione di tasti _CTRL + V_ (incolla). In questo modo tutte le gare di interesse dovrebbero essere state copiate nel file Excel
6. Salvare il file _input.xlsx_ e chiuderlo

Se è stato fatto tutto correttamente, basterà eseguire (doppio click sinistro) il file _GOandUISP.exe_ __nella stessa cartella__ del file _input.xlsx_: dopo qualche secondo verrà creato un file _output.xlsx_ con i dati formattati nel modo desiderato.

__NOTA__: nel caso di atleti con più di un nome/cognome il programma chiederà di inserirli manualmente, comunicandovi tutti i dati che possiede di quel determinato atleta. Potete scrivere sia in maiuscolo che in minuscolo ed inserire spazi (per i nomi/cognomi multipli). Una volta inserito il nome/cognome multiplo richiesto, premere INVIO e ripetere l'azione ogni qualvolta richiesta dal programma. Al termine della procedura la finestra si chiuderà automaticamente.
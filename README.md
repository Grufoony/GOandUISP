# GOandUISP
Script Python per la conversione di file .xlsx da output GoAndSwim a input per il portale online UISP.

## Guida rapida
Per utilizzare il programma è necessario scaricare l'eseguibile dalla [sezione release](https://github.com/Grufoony/GOandUISP/releases) o in alternativa [qui](https://github.com/Grufoony/GOandUISP/releases/download/v1.0.0/GOandUISP.exe).

Una volta scaricato il file _GOandUISP.exe_:
1. __nella stessa cartella__ creare un file excel (_.xlsx_) chiamato _input_, e aprirlo con Excel. Questo file deve essere vuoto per il momento.
2. Una volta aperto il file _input.xlsx_, aprire il file _.GAS_ della manifestazione che si vuole convertire
3. Selezionare le gare di interesse ed entrare in esse (tasto in basso a sinistra di GoAndSwim)
4. Senza dover fare nulla, si dovrebbe essere sul primo atleta dell'elenco. A questo punto eseguire la combinazione di tasti _CTRL + C_ (copia)
5. Andare nel file vuoto _input.xlsx_ nella prima cella in alto a sinistra (la A1) ed eseguirle la combinazione di tasti _CTRL + V_ (incolla). In questo modo tutte le gare di interesse dovrebbero essere state copiate nel file Excel.
6. Salvare il file _input.xlsx_ e chiuderlo.

Infine, se è stato fatto tutto correttamente, basterà eseguire (doppio click sinistro) il file _GOandUISP.exe_: dopo qualche secondo verrà creato un file _output.xlsx_ con i dati formattati nel modo desiderato.
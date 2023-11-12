# GOandUISP
Script Python per la conversione di file _.xlsx_ da output GoAndSwim a input per il portale online UISP.

***

## File gare
Nella sottocartella *races* sono presenti cartelle per varie manifestazioni contenenti file utili per esse.

***

## Ottenere l'eseguibile
Lo script si può eseguire sulla piattaforma [Google Colab](https://colab.research.google.com/github/Grufoony/GOandUISP/blob/main/main.ipynb).

Per qualsiasi problema [scrivimi una mail](mailto:gregorio.berselli@studio.unibo.it).

***

## Accumuli

### Preparare il file di input
1. Creare un file excel (*<nome\>.xlsx*), e aprirlo con Excel. Questo file deve essere vuoto per il momento
2. Una volta aperto il file, aprire il file _.GAS_ della manifestazione che si vuole convertire
3. Selezionare le gare di interesse ed entrare in esse (tasto in basso a sinistra di GoAndSwim)
4. Senza dover fare nulla, si dovrebbe essere sul primo atleta dell'elenco. A questo punto eseguire la combinazione di tasti _CTRL + C_ (copia)
5. Andare nel file vuoto appena creato nella prima cella in alto a sinistra (la A1) ed eseguirle la combinazione di tasti _CTRL + V_ (incolla). In questo modo tutte le gare di interesse dovrebbero essere state copiate nel file Excel
6. Salvare il file e chiuderlo

__NOTA__: nel caso di atleti con più di un nome/cognome il programma chiederà di inserirli manualmente, comunicandovi tutti i dati che possiede di quel determinato atleta. Potete scrivere sia in maiuscolo che in minuscolo ed inserire spazi (per i nomi/cognomi multipli). Una volta inserito il nome/cognome multiplo richiesto, premere INVIO e ripetere l'azione ogni qualvolta richiesta dal programma. Al termine della procedura la finestra si chiuderà automaticamente.

Il file così creato dovrebbe presentarsi nel formato:

|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
|ROSSI MARIO |2013   |M |EB1    |50	    |F	    |Aosta	    |34	|2	 |00'45"30 	 |00'47"10 	|1	|1  |T  |EB1 	|0	|0  |	 
|ROSSI MARIO |2013   |M |EB1 	|100	|D	    |Aosta	    |27	|4	 |01'24"50 	 |01'24"80 	|1	|1	|T  |EB1 	|0	|0  | 
|ROSSI MARIO |2013   |M |EB1 	|200	|R	    |Aosta	    |27	|4	 |01'24"50 	 |01'24"80 	|1	|1	|T  |EB1 	|0	|0	| 
|ROSI MARIA  |2011   |F |EA2 	|100	|S	    |Catanzaro	|10	|1	 |01'16"00 	 |01'17"10 	|1	|1	|S  |EA2 	|0	|0	| 
|ROSI MARIA  |2011   |F |EA2 	|100	|M	    |Catanzaro	|23	|3	 |01'24"00 	 |01'26"90 	|1	|1	|T  |EA2 	|0	|0	|

oppure, nel caso siano presenti staffette nella manifestazione:

|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|<!-- -->|
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
|ROSSI MARIO |              |2013   |M |EB1 |50	    |Aosta	    |F	|34	|2	 |00'45"30 	 |00'47"10 	|1	|1  |T  |EB1 |0	|0  |	 
|ROSSI MARIO |              |2013   |M |EB1 |100	|Aosta	    |D	|27	|4	 |01'24"50 	 |01'24"80 	|1	|1	|T  |EB1 |0	|0  | 
|ROSSI MARIO |              |2013   |M |EB1 |200	|Aosta      |R	|27	|4	 |01'24"50 	 |01'24"80 	|1	|1	|T  |EB1 |0	|0	|
|            |LOMBARDIA ASD	|0		|  |    |100    |           |M	|	|	 |00'30'00	|00'30"00	|1	|1	|T  |    |   | 	|					
|ROSI MARIA  |              |2011   |F |EA2 |100	|Catanzaro	|S	|10	|1	 |01'16"00 	 |01'17"10 	|1	|1	|S  |EA2 |0	|0	| 
|ROSI MARIA  |              |2011   |F |EA2 |100	|Catanzaro	|M	|23	|3	 |01'24"00 	 |01'26"90 	|1	|1	|T  |EA2 |0	|0	|

***

## Generare automaticamente le categorie delle staffette
In questo caso serviranno i due file forniti dal portale nazionale UISP, *<nome\>-dbmeeting.csv* e *<nome\>-staffette-dbmeeting.csv*.
Se presenti nella cartella il programma produrrà in output il file *<nome\>-staffette.csv*.
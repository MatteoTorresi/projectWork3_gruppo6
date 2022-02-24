# projectWork3_gruppo6
Design, Develop and Test an Alexa application that is able to:

- Given the region name,month and year calculate the overall number of doses
  delivered
- Given the month and year calculate the region that received the highest/lowest
  number of doses
- Given a region calculate the average value of delivered doses over the entire dataset

Develop back-end with AWS lambda

Check the following data:

https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json

Analisi:

TASK 1 - Diamo in input il nome della regione, il mese e l'anno di cui vogliamo calcolare il totale dei vaccini fatti.
Controlliamo il nome della regione dato in input con il nome della regione del dizionario dato in json, se questo corrisponde
allora controlliamo se anche il mese e l'anno corrispondono, se quest'ultimi corrispondono a loro volta, allora sommo il numero di dosi effettuati altrimenti
continuo a controlllare.
Infine stampo il numero di dosi effettuate in quel mese dell'anno in quella regione


TASK 2 - Diamo in input la data sottoforma di mese e anno, controlliamo per ogni dizionario se corrisponde con la data inputata, se si allora si controlla se
il numero di dosi ricevute è maggiore di max_dosi o minore di min_dosi a seconda del risultato si cambia il valore massimo e minimo


TASK 3 - Diamo in input il nome della regione, controlliamo il nome della regione con tutti i dizionari, se il nome corrisponde allora facciamo la somma ed
aumentiamo il contatore del numero, infine facciamo la media e stampiamo il valore 


COSE IN PIU':
1) grafico del numero dei vaccini consegnati
2) tipo di vaccino e da chi è stato arrivato, per ogni tipo di vaccino si fa una variabile
3) 

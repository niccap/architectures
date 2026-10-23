# Software Architectures for Enterprise Systems

Questa repository raccoglie il codice sorgente, gli esempi e le esercitazioni del corso **Software Architectures for Enterprise Systems** (Architetture software per sistemi aziendali).

Il materiale accompagna le attività di laboratorio e illustra la realizzazione di servizi web, la comunicazione tra componenti, la persistenza dei dati, la containerizzazione e il deployment di sistemi distribuiti.

## Struttura della repository

| Cartella | Contenuti |
| --- | --- |
| [`lab1/`](lab1/) | Notebook Jupyter ed esempi di utilizzo di API HTTP con Python, incluse richieste a servizi di previsioni meteorologiche. |
| [`lab2/`](lab2/) | Introduzione ai servizi REST con Flask e Waitress: Hello World, gestione di paesi e inventario di automobili. |
| [`lab3/`](lab3/) | Containerizzazione dei servizi REST con Docker. |
| [`lab4/`](lab4/) | Applicazioni client-server, client grafici con Kivy/KivyMD ed esercizi sull'autenticazione. |
| [`lab5/`](lab5/) | Persistenza dei dati con SQLite e MySQL, script di inizializzazione e configurazioni Docker Compose. |
| [`lab6/`](lab6/) | Composizione di servizi per la gestione di un inventario di automobili e la decodifica dei VIN, diagrammi UML ed esempi di deployment con Docker Compose e Kubernetes. |
| [`lab7/`](lab7/) | Comunicazione asincrona con RabbitMQ: produttori e consumatori, code di lavoro, publish/subscribe e routing. |
| [`docker/`](docker/) | Esempi introduttivi di Dockerfile, Docker Compose e Compose Watch. |
| [`kubernetes/`](kubernetes/) | Manifest di esempio per applicazioni e MongoDB, con Deployment, Service, ConfigMap, Secret e configurazione della dashboard. |

## Tecnologie utilizzate

- **Python** e **Jupyter Notebook** per gli esempi e le esercitazioni.
- **Flask**, **Waitress** e **Requests** per esporre e consumare API HTTP.
- **Kivy** e **KivyMD** per i client grafici.
- **SQLite**, **MySQL** e **PyMySQL** per la persistenza dei dati.
- **RabbitMQ** e **Pika** per lo scambio di messaggi.
- **Docker**, **Docker Compose** e **Kubernetes** per containerizzazione e orchestrazione.
- **PlantUML** per i diagrammi di classe e di sequenza.

## Avvio di un primo esempio

Per eseguire il servizio REST dei paesi del laboratorio 2, dalla cartella principale della repository crea un ambiente virtuale e installa le dipendenze necessarie.

Su macOS o Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install flask waitress
python lab2/countries.py
```

Su Windows, attiva l'ambiente virtuale da PowerShell con `.\.venv\Scripts\Activate.ps1`, quindi esegui gli stessi comandi di installazione e avvio.

Il servizio è disponibile su `http://localhost:8080`. Da un altro terminale puoi interrogare l'elenco dei paesi:

```bash
curl http://localhost:8080/countries
```

Interrompi il servizio con `Ctrl+C`.

## Utilizzo dei laboratori

Gli esempi sono indipendenti e possono richiedere dipendenze o servizi aggiuntivi. Consulta il codice, i commenti degli esercizi e gli eventuali Dockerfile, file Compose o manifest Kubernetes presenti nella cartella interessata prima dell'esecuzione.

Per i notebook occorre un ambiente Jupyter; per gli esempi MySQL e RabbitMQ devono essere disponibili i rispettivi server. Gli esempi di containerizzazione richiedono Docker e Docker Compose, mentre quelli Kubernetes richiedono un cluster e `kubectl` configurato.

Molti servizi HTTP usano la porta `8080`: eseguili uno alla volta oppure adatta le porte. Quando un esempio usa file locali con percorsi relativi, avvialo dalla sua cartella.

Il codice e le configurazioni hanno finalità didattiche e costituiscono una base per lo studio e lo svolgimento degli esercizi del corso.

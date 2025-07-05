# :shopping_cart: E-commerce store

Piattaforma di e-commerce per gestione di acquisti, prodotti e ordini dei clienti. La web app è stata realizzata con il
framework python Django per il backend, mentre per il frontend è stato utilizzato Bootstrap.

## :rocket: Funzionalità principali
La web application realizzata consente di effettuare diversi tipi di operazioni a seconda della tipologia di utente.
Sono stati pensati due gruppi di utenti:

* Clienti
* Store managers

### Clienti
Ogni cliente può registrarsi alla piattaforma utilizzando il sistema di autenticazione del sito. Una volta autenticato 
e loggato, può effettuare le seguenti operazioni.
* Cercare/filtrare prodotti nel catalogo dello shop
* Aggiungere/rimuovere prodotti al/dal carello, selezionandone la quantità desiderata
* Aggiungere/rimuovere/modificare recensioni dei prodotti (operazione consentita solo se il prodotto è stato acquistato e consegnato al cliente)
* Aggiungere/rimuovere/modificare uno o più indirizzi di consegna. Ogni cliente può avere più indirizzi ma solo uno di
questi può essere il suo indirizzo principale
* Procedere alla fase di checkout. Il processo di checkout include la scelta dell'indirizzo di spedizione (di default è selezionato
l'indirizzo principale ma è possibile crearne uno nuovo durante la fase di acquisto) e la fase di inserimento dei dati della carta (quest'ultimo simulato)
* Visualizzare e filtrare i suoi ordini per vederne lo stato e i prodotti acquistati
* Visualizzare il suo account, con i relativi dati personali
* Modificare i dati personali del suo account, compreso cambio password
* Eliminare il suo account. Tutti i suoi ordini andranno perduti

### Store managers
Un account store manager può essere creato solo dal superuser che può creare solo store managers.
Ogni store manager ha accesso alla pagina admin di django, avendo l'attributo is_staff = True. Può effettuare login normalmente dal sito.
Le operazioni che può compiere sono:
* Visualizzare il catalogo e filtrare i prodotti
* Modificare i dettagli di un prodotto (quantità, nome, descrizione, prezzo, categoria)
* Aggiungere/eliminare un prodotto o una categoria
* Visualizzare gli ordini dei clienti e cambiare lo stato degli ordini (In lavorazione, spedito, consegnato, cancellato)
* Effettuare operazioni di modifica dei suoi dati personali. Non può eliminare il suo account.

Le operazioni dello store manager possono essere compiute non solo dall'interfaccia del sito ma anche dall'interfaccia admin
di django.

Le funzionalità sopra riportate sono protette con i relativi permessi che possono essere quelli generati di default
da django per le operazioni CRUD (add/delete/change/view prodotti, categorie...) oppure permessi custom aggiunti ad alcuni modelli per 
operazioni più specifiche. Un esempio è il permesso  ``` can_change_order_status``` nella classe order aggiunto
al gruppo store_manager relativo all'aggiornamento dello stato di un ordine.

## :wrench: Setup e avvio del progetto in locale 
Per configurare il progetto in locale e testarlo sui dati presenti nel  ```db.sqlite3 ```, seguire i seguenti passi:

1. **Clona il repository** 
    ```bash
    git clone https://github.com/MattiaBenincasa/eCommerceProject.git
    cd eCommerceProject
    ``` 
2. **Crea e attiva un ambiente Conda**: Crea un ambiente Conda dove installare tutte le dipendenze presenti in ```requirements.txt```
    ```bash
    # Crea un nuovo ambiente Conda con Python 3.13.4
    conda create -n django_ecommerce python=3.13.4

    # Attiva l'ambiente Conda
    conda activate django_ecommerce
    ``` 
3. **Installa le dipendeze:** Installa le dipendenze nel nuovo env Conda
     ```bash
    pip install -r requirements.txt
   ```
4. **Database e Dati di Esempio:**
    Il progetto include un database SQLite pre-popolato (`db.sqlite3`) nella directory radice del repository. Questo consente il test dell'applicazione su dati di esempio (prodotti, categorie, utenti di test).

    **Importante:** Se si vuole usare il database pre-popolato (`db.sqlite3`) non è necessario eseguire alcuna operazione preliminare. Se invece si vuole usare un database vuoto e popolarlo da zero, si può eliminare `db.sqlite3` ed eseguire i seguenti comandi: 
    ```bash
    # Per aggiornare lo schema del db
    python manage.py migrate
   
    # Per configurare i gruppi utenti predefiniti ed i loro permessi
    python manage.py shell < setup_groups_permissions.py    
   
    # Per creare un nuovo superuser
    python manage.py createsuperuser
    ```
    
    Per le credenziale e l'accesso alla pagina admin con i dati presenti nel database pre popolato vedere la sezione [Accedere all'amministrazione (account di esempio)](#file_cabinet-accedere-allamministrazione-account-di-esempio).
5. **Avvia il server di sviluppo:**
    ```bash
    python manage.py runserver
    ```
    L'applicazione sarà ora accessibile nel tuo browser all'indirizzo: `http://127.0.0.1:8000/`.

## :file_cabinet: Accedere all'amministrazione (account di esempio)

Per accedere al pannello di amministrazione (`http://127.0.0.1:8000/admin/`) e testare diversi tipi di account, si può utilizzare le seguenti credenziali di esempio:

* **Account Superuser:**
    * **Nome Utente:** `admin`
    * **Password:** `adminpassword`

* **Account Store manager:**
    * **Nome Utente:** `store_manager`
    * **Password:** `stmnpassword`

* **Account Cliente 1:**
    * **Nome Utente:** `test_user_1`
    * **Password:** `testuser1password`
  
* **Account Cliente 2:**
    * **Nome Utente:** `test_user_2`
    * **Password:** `testuser2password`

**AVVISO DI SICUREZZA:**
Queste credenziali sono solo a scopo di test e dimostrazione.

## :gear: Utilizzo

Una volta effettuato il [Setup](#wrench-setup-e-avvio-del-progetto-in-locale) è possibile provare le [funzionalità del sito](#rocket-funzionalità-principali).
Ad esempio, se si effettua il login con l'account Cliente, si può ricercare prodotti dalla barra di ricerca o filtrare le varie categorie con il bottone 'Filtri' nella homepage; si 
possono aggiungere prodotti al carrello e procedere con il checkout.
Se si effettua il login con l'account Store manager si può aggiungere/modificare/rimuovere prodotti oppure modificare lo stato
degli ordini del Cliente. 
Se si effettua il login con l'account Superuser si può ad esempio aggiungere nuovi Store Manager dall'interfaccia admin di django.

Deployment link: https://ecommerceproject-production-9f2e.up.railway.app/
(per la produzione sono state cambiate le credenziali dello store manager e del superuser)
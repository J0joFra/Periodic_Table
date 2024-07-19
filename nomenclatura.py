import pymongo
import pandas as pd

# Funzione per connettersi a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]
    collezione_elementi = db["elementi"]
    return collezione_elementi

# Funzione che analizza il composto ricercato
def analisi_composto(composto, collezione_elementi):
    divisione = composto.split(" ")

    # Controllo lunghezza
    if len(divisione) <= 3:
        # Controllo se è un composto binario               
        if divisione[0].endswith("uro"):
            print(f"Il {composto} è un composto binario perchè ha il suffisso -uro")
            composto_binario(divisione, collezione_elementi)            
    return divisione

# Funzione per i composti binari
def composto_binario(divisione, collezione_elementi):
    # Controlla la presenza di 'di'
    if 'di' in divisione:
        divisione.remove('di')
    # Unità positiva   
    el_1 = divisione[1] 
    
    # Controlla se è un "Idruro"
    if divisione[0].startswith('idr'):
        el_2 = 'Idrogeno'
        formula = formatta_idruro(el_1, collezione_elementi)
    # Controlla se è un "Solfuro"
    elif divisione[0].startswith('solf'):
        el_2 = 'Zolfo'
        formula = f"S{cerca_simbolo(el_1.capitalize(), collezione_elementi)}"
    else:
        el_parziale = divisione[0].removesuffix('uro')
        el = el_parziale.capitalize()
        # Secondo elemento
        el_2 = cerca_elemento(el, collezione_elementi)
        formula = f"{cerca_simbolo(el_2, collezione_elementi)}{cerca_simbolo(el_1.capitalize(), collezione_elementi)}"
    
    if el_2:
        print(f"Il {composto} è composto da {el_2} + {el_1}")
        print(f"Formula: {formula}")
        
        # Calcolo e stampa del numero di ossidazione
        n_ox_1 = calcola_numero_ossidazione(el_1.capitalize(), collezione_elementi)
        n_ox_2 = calcola_numero_ossidazione(el_2, collezione_elementi)
        print(f"Numero di ossidazione di {el_1}: {n_ox_1}")
        print(f"Numero di ossidazione di {el_2}: {n_ox_2}")
    else:
        print(f"Simbolo non trovato per uno o entrambi gli elementi")

# Funzione per cercare il nome completo di un elemento  
def cerca_elemento(el, collezione_elementi):
    elementi = collezione_elementi.find()
    for elemento in elementi:
        # Recupera tutti i nomi italiani
        nome_elemento = elemento.get("name_italian", "")
        
        # Nome senza suffisso da cercare
        if nome_elemento.startswith(el):
            # Salvataggio nome completo
            return nome_elemento
    
    return None

# Funzione per ottenere i simboli di un elemento
def cerca_simbolo(nome, collezione_elementi):
    elementi = collezione_elementi.find()
    for elemento in elementi:
        # Recupera il nome dell'elemento
        nome_elemento = elemento.get("name_italian", "")
        # Recupera il simbolo dell'elemento
        simbolo_elemento = elemento.get("symbol", "")
        
        # Controlla se il nome dell'elemento corrisponde al nome dato
        if nome_elemento.lower() == nome.lower():
            return simbolo_elemento
    
    return None

# Funzione per determinare gli idruri
def formatta_idruro(el_1, collezione_elementi):
    elementi = collezione_elementi.find()
    for elemento in elementi:
        # Recupera il nome dell'elemento
        nome_elemento = elemento.get("name_italian", "")
        # Recupera il gruppo dell'elemento
        gruppo_elemento = elemento.get("group_id", "")
        # Recupera il simbolo dell'elemento
        simbolo_elemento = elemento.get("symbol", "")
        
        if nome_elemento.lower() == el_1.lower():
            if gruppo_elemento in [1, 2] and nome_elemento not in ['Litio', 'Berillio']:
                # Idruri metallici
                formula = f"{simbolo_elemento}H"
                print(f"Idruro metallico: {formula}")
            else:
                # Idruri covalenti
                formula = f"H{simbolo_elemento}"
                print(f"Idruro covalente: {formula}")
            return formula
    return None

# Funzione per calcolare il numero di ossidazione
def calcola_numero_ossidazione(el, collezione_elementi):
    elemento = collezione_elementi.find_one({"name_italian": el})
    if elemento:
        n_ox_list = elemento.get("oxidation_states", [])
        if n_ox_list:
            return n_ox_list
    return None

# URI di connessione a MongoDB
mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
collezione_elementi = connect_to_mongodb(mongo_uri)

# Composto da ricercare
composto = input("Inserisci il nome di un composto: ").lower()

# Analizzo il composto
analisi_composto(composto, collezione_elementi)

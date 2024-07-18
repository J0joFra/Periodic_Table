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
    # Controllo la presenza di 'di'
    if 'di' in divisione:
        divisione.remove('di') # Rimozione di 'di'
    el_1 = divisione[1] #unità positiva
    
    el_parziale = divisione[0].removesuffix('uro')
    el = el_parziale.capitalize()
    # Secondo elemento
    el_2 = cerca_elemento(el, collezione_elementi)
    
    print(f"Il {composto} è composto da {el_2} + {el_1}")
    
    # Costruzione della formula
    simbolo_el_1 = cerca_simbolo(el_1.capitalize(), collezione_elementi)
    simbolo_el_2 = cerca_simbolo(el_2, collezione_elementi)
    
    if simbolo_el_1 and simbolo_el_2:
        print(f"{simbolo_el_1}{simbolo_el_2}")
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

# URI di connessione a MongoDB
mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
collezione_elementi = connect_to_mongodb(mongo_uri)

# Composto da ricercare
composto = input("Inserisci il nome di un composto: ").lower()

# Analizzo il composto
analisi_composto(composto, collezione_elementi)

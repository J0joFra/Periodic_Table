import pymongo
import pandas as pd

# Funzione che analizza il composto ricercato
def analisi_composto(composto):
    divisione = composto.split(" ")
    
    # Controllo lunghezza
    if len(divisione) <= 3:
        # Controllo se è un composto binario               
        if divisione[0].endswith("uro"):
            print(f"Il {composto} è un composto binario perchè ha il suffisso -uro")
            composto_binario(divisione)            
    return divisione

# Funzione per i composti binari
def composto_binario(divisione):
    # Controllo la presenza di 'di'
    if divisione[1] == 'di':
        divisione.remove('di') # Rimozione di 'di'
    el_1 = divisione[1] #unità positiva (metallo)
    el_parziale = divisione[0].removesuffix('uro')
    el = el_parziale.capitalize()
    print(f"{el_1} + {el_parziale}")

# Funzione per cercare il nome completo di un elemento  
def cerca_elemento(el):
    # Recupera tutti gli elementi
    elementi = collezione_elementi.find()
    
    for elemento in elementi:
        # Recupera tutti i nomi italiani
        nome_elemento = elemento.get("name_italian")
        
        # Nome senza suffisso da cercare
        if nome_elemento.startwith(el):
            # Salvataggio nome completo
            el_2 = nome_elemento
            print(el_2)
        else:
            print("Non trovato")
    return el_2
    
# Composto da ricercare
composto = input("Inserisci il nome di un composto: ").lower()
# Analizzo il composto
analisi_composto(composto)


import pymongo
import pandas as pd

# Funzione che analizza il composto ricercato
def analisi_composto(composto):
    divisione = composto.split(" ")
    
    # Controllo se è un composto binario
    if len(divisione) <= 3: 
        if divisione[0].endswith("uro"):
            print("Composto binario")
    print(divisione)
    return divisione

# Composto da ricercare
composto = input("Inserisci il nome di un composto: ")

analisi_composto(composto)


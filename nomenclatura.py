import pymongo
import pandas as pd

# Funzione che analizza il composto ricercato
def analisi_composto(composto):
    divisione = composto.split(" ")
    
    # Controllo se è un composto binario
    if len(divisione) <= 3: 
        if divisione[0].endswith("uro"):
            print(f"il {composto} è un composto binario perchè ha il suffisso -uro")
            composto_binario(divisione)
    return divisione

# Funzione per i composti binari
def composto_binario(divisione):
    print("Ciao")
    
# Composto da ricercare
composto = input("Inserisci il nome di un composto: ")

analisi_composto(composto)


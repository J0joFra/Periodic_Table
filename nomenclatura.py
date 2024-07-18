import pymongo
import pandas as pd

# Funzione che analizza il composto ricercato
def analisi_composto(composto):
    divisione = composto.split(" ")
    if len(divisione) == 3:
        print("Possibile binario")
    print(divisione)
    return divisione

# Composto da ricercare
composto = input("Inserisci il nome di un composto: ")

analisi_composto(composto)


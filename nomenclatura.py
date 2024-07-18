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
    if 'di' in divisione[1]:
        divisione.remove('di') # Rimozione di 'di'
    print("Ciao")
    
# Composto da ricercare
composto = input("Inserisci il nome di un composto: ").lower()
# Analizzo il composto
analisi_composto(composto)


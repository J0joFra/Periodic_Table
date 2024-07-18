import pymongo

# Connessione a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elementi"]  # Nome della collezione degli elementi
    return collezione_elementi

# Dizionario di mappatura dei nomi italiani agli equivalenti inglesi
italiano_to_inglese = {
    "idrogeno": "hydrogen",
    "cloro": "chlorine",
    "zolfo": "sulfur",
    "sodio": "sodium",
    "potassio": "potassium",
    "bromo": "bromine",
    # Aggiungi altri elementi secondo necessità
}

# Funzione per ottenere la formula chimica dal nome IUPAC
def get_formula_chimica(nome_iupac, collezione_elementi):
    # Separare le parole del nome IUPAC
    parole = nome_iupac.split()
    
    if len(parole) < 3 or parole[1] != "di":
        return "Nome IUPAC non valido"
    
    nome_non_metallo_italiano = parole[0][:-3].lower()  # Rimuove il suffisso -uro e converte in minuscolo
    nome_metallo_italiano = parole[-1].lower()  # L'ultimo termine è il nome del metallo

    # Convertire i nomi italiani in inglese
    nome_non_metallo = italiano_to_inglese.get(nome_non_metallo_italiano)
    nome_metallo = italiano_to_inglese.get(nome_metallo_italiano)
    
    if not nome_non_metallo or not nome_metallo:
        return "Elemento non trovato nella mappatura"

    # Trovare i simboli nel database
    non_metallo = collezione_elementi.find_one({"name": nome_non_metallo})
    metallo = collezione_elementi.find_one({"name": nome_metallo})
    
    if not non_metallo or not metallo:
        return "Elemento non trovato nel database"

    simbolo_non_metallo = non_metallo["symbol"]
    simbolo_metallo = metallo["symbol"]

    return f"{simbolo_metallo}{simbolo_non_metallo}"

# Esempio di utilizzo
def main():
    # URI di connessione a MongoDB Atlas (sostituisci con il tuo URI)
    mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
    collezione_elementi = connect_to_mongodb(mongo_uri)

    # Esempi di nomi IUPAC
    nomi_iupac = ["cloruro di idrogeno", "solfuro di idrogeno", "cloruro di sodio", "bromuro di potassio"]
    for nome in nomi_iupac:
        formula_chimica = get_formula_chimica(nome, collezione_elementi)
        print(f"La formula chimica di {nome} è: {formula_chimica}")

if __name__ == "__main__":
    main()

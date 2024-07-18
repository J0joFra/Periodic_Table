import pymongo

# Connessione a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elementi"]  # Nome della collezione degli elementi
    return collezione_elementi

# Funzione per ottenere la formula chimica dal nome IUPAC
def get_formula_chimica(nome_iupac, collezione_elementi):
    # Dividi il nome IUPAC in parole
    parole = nome_iupac.split()
    
    formula_chimica = []
    for parola in parole:
        # Trova l'elemento corrispondente nella collezione MongoDB
        elemento = collezione_elementi.find_one({"nome": parola.lower()})
        if elemento:
            formula_chimica.append(elemento["simbolo"])
        else:
            return f"Elemento non trovato per il nome {parola}"

    return ''.join(formula_chimica)

# Esempio di utilizzo
def main():
    # URI di connessione a MongoDB Atlas (sostituisci con il tuo URI)
    mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
    collezione_elementi = connect_to_mongodb(mongo_uri)

    nome_iupac = "ossido di magnesio"  # Nome IUPAC della molecola da analizzare
    formula_chimica = get_formula_chimica(nome_iupac, collezione_elementi)
    print(f"La formula chimica di {nome_iupac} è: {formula_chimica}")

if __name__ == "__main__":
    main()

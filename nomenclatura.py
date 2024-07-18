import pymongo

# Connessione a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elementi"]  # Nome della collezione degli elementi
    return collezione_elementi

# Funzione per ottenere il nome IUPAC della molecola
def get_nome_iupac(molecola, collezione_elementi):
    # Divide la molecola nei suoi componenti (ad esempio: CH3CH2OH -> ['C', 'H', 'C', 'H', 'O', 'H'])
    componenti = []
    i = 0
    while i < len(molecola):
        if i + 1 < len(molecola) and molecola[i + 1].islower():
            componenti.append(molecola[i:i + 2])
            i += 2
        else:
            componenti.append(molecola[i])
            i += 1

    # Trova il nome IUPAC della molecola utilizzando i dati degli elementi chimici da MongoDB
    nome_iupac = []
    for composto in componenti:
        elemento = collezione_elementi.find_one({"simbolo": composto})
        if elemento:
            nome_iupac.append(elemento["nome"])
        else:
            return "Nome IUPAC non trovato per la molecola"

    return ''.join(nome_iupac)

# Esempio di utilizzo
def main():
    # URI di connessione a MongoDB Atlas (sostituisci con il tuo URI)
    mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
    collezione_elementi = connect_to_mongodb(mongo_uri)

    molecola = "CH3CH2OH"  # Formula chimica della molecola da analizzare
    nome_iupac = get_nome_iupac(molecola, collezione_elementi)
    print(f"Il nome IUPAC della molecola {molecola} è: {nome_iupac}")

if __name__ == "__main__":
    main()


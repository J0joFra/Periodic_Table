import pymongo

# Connessione a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elementi"]  # Nome della collezione degli elementi
    return collezione_elementi

# Dizionario dei prefissi IUPAC
prefissi_iupac = {
    "mono": 1,
    "di": 2,
    "tri": 3,
    "tetra": 4,
    "penta": 5,
    "esa": 6,
    "epta": 7,
    "otta": 8,
    "nona": 9,
    "deca": 10
}

# Funzione per ottenere la formula chimica dal nome IUPAC
def get_formula_chimica(nome_iupac, collezione_elementi):
    # Dividi il nome IUPAC in parole
    parole = nome_iupac.split()
    
    formula_chimica = []
    i = 0
    while i < len(parole):
        # Trova l'elemento corrispondente nella collezione MongoDB
        elemento = collezione_elementi.find_one({"nome": parole[i].lower()})
        if elemento:
            simbolo = elemento["simbolo"]
            # Controlla se la prossima parola è un prefisso
            if i + 1 < len(parole) and parole[i + 1].lower() in prefissi_iupac:
                prefisso = prefissi_iupac[parole[i + 1].lower()]
                formula_chimica.append(f"{simbolo}{prefisso if prefisso > 1 else ''}")
                i += 1  # Salta il prefisso
            else:
                formula_chimica.append(simbolo)
        else:
            return f"Elemento non trovato per il nome {parole[i]}"
        i += 1

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

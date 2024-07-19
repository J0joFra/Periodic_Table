import pymongo
import re

# Funzione per connettersi a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]
    collezione_elementi = db["elementi"]
    return collezione_elementi

# Funzione per cercare il nome completo di un elemento
def cerca_elemento(simbolo, collezione_elementi):
    elemento = collezione_elementi.find_one({"symbol": simbolo})
    if elemento:
        return elemento.get("name_italian", "")
    return None

# Funzione per analizzare la formula chimica
def analizza_formula(formula, collezione_elementi):
    pattern = r"([A-Z][a-z]*)(\d*)"
    matches = re.findall(pattern, formula)
    
    elementi = []
    for match in matches:
        simbolo, quantita = match
        nome_elemento = cerca_elemento(simbolo, collezione_elementi)
        if nome_elemento:
            quantita = int(quantita) if quantita else 1
            elementi.append((nome_elemento, quantita))
    
    return elementi

# Funzione per generare il nome del composto
def genera_nome(elementi):
    if len(elementi) == 2:
        el_1, el_2 = elementi
        nome_1, quantita_2 = el_2
        nome_2, quantita_1 = el_1
        
        # Togli l'ultima lettera dal nome dell'elemento anionico prima di aggiungere -uro
        nome_1_modificato = nome_1[:-1] + 'uro'
        
        # Regole IUPAC per composti binari
        if quantita_2 == 1:
            nome_composto = f"{nome_1_modificato} di {nome_2}"
        else:
            nome_composto = f"{nome_1_modificato} di {nome_2} ({quantita_2})"
        return nome_composto
    return "Composto non riconosciuto"

# URI di connessione a MongoDB
mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
collezione_elementi = connect_to_mongodb(mongo_uri)

# Formula da ricercare
formula = input("Inserisci la formula di un composto: ")

# Analizzo la formula
elementi = analizza_formula(formula, collezione_elementi)

# Genero il nome del composto
nome_composto = genera_nome(elementi)
print(f"Il nome del composto è: {nome_composto}")

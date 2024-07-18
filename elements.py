import pymongo
import pandas as pd

# Connessione a MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Creazione o selezione del database
db = client["tavola_periodica"]

# Creazione o selezione della collezione per gli elementi chimici
collezione_elementi = db["elementi"]

# Lettura dei dati dal CSV con Pandas (esempio)
df = pd.read_csv('elementi_chimici.csv')


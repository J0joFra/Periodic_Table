import pymongo
import pandas as pd

# Connessione a MongoDB
client = pymongo.MongoClient("mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/")

# Creazione o selezione del database
db = client["tavola_periodica"]

# Creazione o selezione della collezione per gli elementi chimici
collezione_elementi = db["elementi"]

# Lettura dei dati dal CSV
df = pd.read_csv(r'C:\Users\JoaquimFrancalanci\OneDrive - ITS Angelo Rizzoli\Documenti\GitHub\IUPAC_name\Data\elemtents.csv')

# Inserimento dei dati nella collezione MongoDB
elementi_da_inserire = df.to_dict(orient='records')
collezione_elementi.insert_many(elementi_da_inserire)

# Chiusura della connessione a MongoDB
client.close()

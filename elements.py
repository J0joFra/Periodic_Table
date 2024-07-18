import pymongo
from googletrans import Translator
import pandas as pd

def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elementi"]  # Nome della collezione degli elementi
    return collezione_elementi

def create_db():
    # Creazione del database
    db = client["tavola_periodica"]

    # Creazione della collezione per gli elementi
    collezione_elementi = db["elementi"]

    df = pd.read_csv(r'C:\Users\JoaquimFrancalanci\OneDrive - ITS Angelo Rizzoli\Documenti\GitHub\IUPAC_name\Data\elemtents.csv')

    # Inserimento dei dati nella collezione MongoDB
    elementi_da_inserire = df.to_dict(orient='records')
    collezione_elementi.insert_many(elementi_da_inserire)
    return collezione_elementi

def traduci_elementi(collezione_elementi):
    translator = Translator()

    # Recupera tutti gli elementi
    elementi = collezione_elementi.find()

    for elemento in elementi:
        nome_inglese = elemento.get("name")
        
        if nome_inglese:
            # Traduci il nome in italiano
            traduzione = translator.translate(nome_inglese, src='en', dest='it')
            nome_italiano = traduzione.text
            
            # Aggiorna il documento nel database
            collezione_elementi.update_one(
                {"_id": elemento["_id"]},
                {"$set": {"name_italian": nome_italiano}}
            )
            print(f"Elemento aggiornato: {nome_inglese} -> {nome_italiano}")

def main():
    # URI di connessione a MongoDB Atlas
    mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
    collezione_elementi = connect_to_mongodb(mongo_uri)
    
    # Crea/seleziona DB
    create_db()
    
    # Traduce e aggiorna i nomi degli elementi
    traduci_elementi(collezione_elementi)
    
    # Chiusura della connessione a MongoDB
    client.close()

if __name__ == "__main__":
    main()
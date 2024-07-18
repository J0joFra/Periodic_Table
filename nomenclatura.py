import pymongo
from googletrans import Translator

def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elementi"]  # Nome della collezione degli elementi
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
    
    # Traduci e aggiorna i nomi degli elementi
    traduci_elementi(collezione_elementi)

if __name__ == "__main__":
    main()

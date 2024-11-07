import pymongo
import re

# Funzione per connettersi a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]
    collezione_elementi = db["elementi"]
    return collezione_elementi


# URI di connessione a MongoDB
mongo_uri = "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/"
collezione_elementi = connect_to_mongodb(mongo_uri)


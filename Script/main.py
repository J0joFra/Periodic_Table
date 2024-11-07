import pymongo
from flask import Flask, jsonify, request
import re
import os

# Funzione per connettersi a MongoDB
def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]
    collezione_elementi = db["elementi"]
    return collezione_elementi

# URI di connessione a MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://jofrancalanci:Cf8m2xsQdZgll1hz@element.2o7dxct.mongodb.net/")
collezione_elementi = connect_to_mongodb(mongo_uri)

# Creazione dell'app Flask
app = Flask(__name__)

# Route per ottenere tutti gli elementi della tavola periodica
@app.route('/elementi', methods=['GET'])
def get_all_elements():
    elementi = list(collezione_elementi.find({}, {"_id": 0}))  # Esclude il campo '_id'
    return jsonify(elementi)

# Route per ottenere elementi filtrati in base a una caratteristica specifica
@app.route('/elementi/<caratteristica>', methods=['GET'])
def get_elements_by_characteristic(caratteristica):
    # Parametro per il valore minimo della caratteristica (es: 'valore_min')
    valore_min = request.args.get("valore_min", type=float, default=None)
    query = {}

    if valore_min is not None:
        query[caratteristica] = {"$gte": valore_min}

    elementi = list(collezione_elementi.find(query, {"_id": 0, caratteristica: 1, "nome": 1}))
    return jsonify(elementi)

# Route per cercare un elemento per nome o simbolo
@app.route('/elementi/cerca', methods=['GET'])
def search_element():
    query_param = request.args.get("query", "")
    query = {
        "$or": [
            {"nome": {"$regex": re.compile(query_param, re.IGNORECASE)}},
            {"simbolo": {"$regex": re.compile(query_param, re.IGNORECASE)}}
        ]
    }

    elementi = list(collezione_elementi.find(query, {"_id": 0}))
    return jsonify(elementi)

if __name__ == "__main__":
    # Avvia il server Flask
    app.run(host="0.0.0.0", port=5000)

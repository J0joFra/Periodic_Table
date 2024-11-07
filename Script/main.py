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

# Route principale per confermare che il server è in esecuzione
@app.route('/', methods=['GET'])
def index():
    return "Server Flask in esecuzione!"

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Route per ottenere tutti gli elementi della tavola periodica
@app.route('/elementi', methods=['GET'])
def get_all_elements():
    elementi = list(collezione_elementi.find({}, {"_id": 0}))  # Esclude il campo '_id'
    return jsonify(elementi)

# Route per ottenere elementi con una caratteristica specifica in rilievo
@app.route('/elementi/<caratteristica>', methods=['GET'])
def get_elements_by_characteristic(caratteristica):
    valore_min = request.args.get("valore_min", type=float, default=None)
    query = {}

    # Controllo se la caratteristica è presente e se un valore minimo è fornito
    if valore_min is not None:
        query[caratteristica] = {"$gte": valore_min}

    elementi = list(collezione_elementi.find(query, {"_id": 0, caratteristica: 1, "name": 1, "symbol": 1}))
    return jsonify(elementi)

# Route per cercare un elemento per nome, simbolo o numero atomico
@app.route('/elementi/cerca', methods=['GET'])
def search_element():
    query_param = request.args.get("query", "")
    query = {
        "$or": [
            {"name": {"$regex": re.compile(query_param, re.IGNORECASE)}},
            {"symbol": {"$regex": re.compile(query_param, re.IGNORECASE)}},
            {"atomic_number": int(query_param) if query_param.isdigit() else None}
        ]
    }

    elementi = list(collezione_elementi.find(query, {"_id": 0}))
    return jsonify(elementi)

# Route per ottenere proprietà dettagliate di un singolo elemento dato il simbolo
@app.route('/elemento/<simbolo>', methods=['GET'])
def get_element_details(simbolo):
    elemento = collezione_elementi.find_one({"symbol": simbolo}, {"_id": 0})
    if elemento:
        return jsonify(elemento)
    else:
        return jsonify({"error": "Elemento non trovato"}), 404

if __name__ == "__main__":
    # Avvia il server Flask
    app.run(host="0.0.0.0", port=5000)

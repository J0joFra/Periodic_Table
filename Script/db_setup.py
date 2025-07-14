import pymongo
from googletrans import Translator
import pandas as pd

def connect_to_mongodb(uri):
    client = pymongo.MongoClient(uri)
    db = client["tavola_periodica"]  # Nome del database
    collezione_elementi = db["elements"]  # Nome della collezione degli elementi
    return client, collezione_elementi

def create_db(client):
    # Creazione del database
    db = client["tavola_periodica"]

    # Creazione della collezione per gli elementi
    collezione_elementi = db["elementi"]

    df = pd.read_csv("elements.csv") 
    
    # Inserimento dei dati nella collezione MongoDB
    elementi_da_inserire = df.to_dict(orient='records')
    collezione_elementi.insert_many(elementi_da_inserire)
    return collezione_elementi

def aggiungi_numeri_ossidazione(collezione_elementi, numeri_ossidazione):
    for elemento in collezione_elementi.find():
        nome_inglese = elemento.get("name")
        if nome_inglese in numeri_ossidazione:
            collezione_elementi.update_one(
                {"_id": elemento["_id"]},
                {"$set": {"oxidation_states": numeri_ossidazione[nome_inglese]}}
            )
            print(f"Stati di ossidazione aggiornati per: {nome_inglese}")

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
    mongo_uri = "mongodb+srv://jofrancalanci:d9T9r1EJtHAWQP6U@chimica.m7qhhot.mongodb.net/"
    client, collezione_elementi = connect_to_mongodb(mongo_uri)
    
    # Crea/seleziona DB
    create_db(client)
    
    # Numeri di ossidazione per gli elementi
    numeri_ossidazione = {
        "Hydrogen": [+1, -1],
        "Helium": [0],
        "Lithium": [+1],
        "Beryllium": [+2],
        "Boron": [+3],
        "Carbon": [-4, -3, -2, -1, +1, +2, +3, +4],
        "Nitrogen": [-3, -2, -1, +1, +2, +3, +4, +5],
        "Oxygen": [-2, -1, +1, +2],
        "Fluorine": [-1],
        "Neon": [0],
        "Sodium": [+1],
        "Magnesium": [+2],
        "Aluminum": [+3],
        "Silicon": [-4, -3, -2, -1, +1, +2, +3, +4],
        "Phosphorus": [-3, +1, +3, +5],
        "Sulfur": [-2, +2, +4, +6],
        "Chlorine": [-1, +1, +3, +5, +7],
        "Argon": [0],
        "Potassium": [+1],
        "Calcium": [+2],
        "Scandium": [+3],
        "Titanium": [+2, +3, +4],
        "Vanadium": [+2, +3, +4, +5],
        "Chromium": [+2, +3, +6],
        "Manganese": [+2, +3, +4, +6, +7],
        "Iron": [+2, +3],
        "Cobalt": [+2, +3],
        "Nickel": [+2, +3],
        "Copper": [+1, +2],
        "Zinc": [+2],
        "Gallium": [+3],
        "Germanium": [+2, +4],
        "Arsenic": [-3, +3, +5],
        "Selenium": [-2, +4, +6],
        "Bromine": [-1, +1, +3, +5],
        "Krypton": [0, +2],
        "Rubidium": [+1],
        "Strontium": [+2],
        "Yttrium": [+3],
        "Zirconium": [+4],
        "Niobium": [+3, +5],
        "Molybdenum": [+2, +3, +4, +5, +6],
        "Technetium": [+4, +7],
        "Ruthenium": [+2, +3, +4, +6, +8],
        "Rhodium": [+2, +3, +4],
        "Palladium": [+2, +4],
        "Silver": [+1, +2],
        "Cadmium": [+2],
        "Indium": [+3],
        "Tin": [+2, +4],
        "Antimony": [-3, +3, +5],
        "Tellurium": [-2, +4, +6],
        "Iodine": [-1, +1, +3, +5, +7],
        "Xenon": [0, +2, +4, +6, +8],
        "Cesium": [+1],
        "Barium": [+2],
        "Lanthanum": [+3],
        "Cerium": [+3, +4],
        "Praseodymium": [+3, +4],
        "Neodymium": [+3],
        "Promethium": [+3],
        "Samarium": [+2, +3],
        "Europium": [+2, +3],
        "Gadolinium": [+3],
        "Terbium": [+3, +4],
        "Dysprosium": [+3],
        "Holmium": [+3],
        "Erbium": [+3],
        "Thulium": [+2, +3],
        "Ytterbium": [+2, +3],
        "Lutetium": [+3],
        "Hafnium": [+4],
        "Tantalum": [+5],
        "Tungsten": [+2, +3, +4, +5, +6],
        "Rhenium": [+2, +4, +6, +7],
        "Osmium": [+2, +3, +4, +6, +8],
        "Iridium": [+2, +3, +4, +6],
        "Platinum": [+2, +4],
        "Gold": [+1, +3],
        "Mercury": [+1, +2],
        "Thallium": [+1, +3],
        "Lead": [+2, +4],
        "Bismuth": [+3, +5],
        "Polonium": [+2, +4, +6],
        "Astatine": [-1, +1, +3, +5, +7],
        "Radon": [0],
        "Francium": [+1],
        "Radium": [+2],
        "Actinium": [+3],
        "Thorium": [+4],
        "Protactinium": [+5],
        "Uranium": [+3, +4, +5, +6],
        "Neptunium": [+3, +4, +5, +6, +7],
        "Plutonium": [+3, +4, +5, +6],
        "Americium": [+2, +3, +4, +5, +6],
        "Curium": [+3, +4],
        "Berkelium": [+3, +4],
        "Californium": [+2, +3, +4],
        "Einsteinium": [+3],
        "Fermium": [+3],
        "Mendelevium": [+2, +3],
        "Nobelium": [+2, +3],
        "Lawrencium": [+3],
        "Rutherfordium": [+4],
        "Dubnium": [+5],
        "Seaborgium": [+6],
        "Bohrium": [+7],
        "Hassium": [+8],
        "Meitnerium": [+1, +3],
        "Darmstadtium": [+2, +4, +6, +8],
        "Roentgenium": [+1, +3],
        "Copernicium": [+2],
        "Nihonium": [+1, +3, +5],
        "Flerovium": [+2, +4],
        "Moscovium": [+1, +3],
        "Livermorium": [+2, +4],
        "Tennessine": [-1, +1, +3, +5, +7],
        "Oganesson": [0]
    }
    
    # Aggiungi i numeri di ossidazione agli elementi
    aggiungi_numeri_ossidazione(collezione_elementi, numeri_ossidazione)
    
    # Traduce e aggiorna i nomi degli elementi
    traduci_elementi(collezione_elementi)
    
    # Chiusura della connessione a MongoDB
    client.close()

if __name__ == "__main__":
    main()

import re
import requests
from io import BytesIO
from PIL import Image

# Funzione per estrarre elementi chimici e quantità
def estrai_elementi(formula):
    matches = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    elementi = {}
    for simbolo, quantità in matches:
        quantità = int(quantità) if quantità else 1
        if simbolo in elementi:
            elementi[simbolo] += quantità
        else:
            elementi[simbolo] = quantità
    return elementi

# Funzione per classificare il composto inorganico
def classifica_composto(formula, elementi):
    metalli = ['Na', 'K', 'Ca', 'Mg', 'Fe', 'Al', 'Cu', 'Zn', 'Ag', 'Ba', 'Pb', 'Hg']
    non_metalli = ['H', 'O', 'N', 'Cl', 'Br', 'I', 'F', 'S', 'P', 'C']

    keys = list(elementi.keys())

    if 'O' in elementi and len(keys) == 2:
        if any(k in metalli for k in keys if k != 'O'):
            return "Ossido basico"
        elif any(k in non_metalli for k in keys if k != 'O'):
            return "Anidride (ossido acido)"
    if 'OH' in formula or 'OH' in keys:
        return "Base (idrossido)"
    if formula.startswith('H') and 'O' not in formula:
        return "Acido binario"
    if formula.startswith('H') and 'O' in formula:
        return "Acido ossiacido"
    if 'H' in elementi and any(k in metalli for k in keys if k != 'H'):
        return "Idruro metallico"
    if all(k in non_metalli for k in keys):
        return "Composto molecolare"
    if any(k in metalli for k in keys) and any(k in non_metalli for k in keys):
        return "Sale binario o ossosale"
    return "Tipo non identificato"

# Funzione per ottenere info da PubChem
def ottieni_info_pubchem(formula):
    try:
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{formula}/property/IUPACName,MolecularFormula,MolecularWeight/JSON"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        props = data['PropertyTable']['Properties'][0]
        return {
            "iupac": props.get("IUPACName", "Non trovato"),
            "peso_molecolare": props.get("MolecularWeight", "N/D"),
            "formula_molecolare": props.get("MolecularFormula", "N/D")
        }
    except Exception:
        return {
            "iupac": "Non trovato",
            "peso_molecolare": "N/D",
            "formula_molecolare": "N/D"
        }

# Mostra l’immagine della struttura chimica
def mostra_immagine(formula):
    try:
        image_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{formula}/PNG"
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image.show()
    except:
        print("❌ Impossibile mostrare l'immagine della struttura.")

# Funzione principale
def analizza_formula(formula):
    formula = formula.strip()
    print(f"🔬 Formula: {formula}")

    elementi = estrai_elementi(formula)
    print("\n🧪 Elementi presenti:")
    for el, n in elementi.items():
        print(f"  - {el}: {n}")

    tipo = classifica_composto(formula, elementi)
    print(f"\n📂 Tipo di composto: {tipo}")

    info = ottieni_info_pubchem(formula)
    print("\n📘 Informazioni da PubChem:")
    print(f"  - Nome IUPAC: {info['iupac']}")
    print(f"  - Formula molecolare: {info['formula_molecolare']}")
    print(f"  - Peso molecolare: {info['peso_molecolare']}")

    mostra_immagine(formula)

# Esecuzione
if __name__ == "__main__":
    formula_input = input("Inserisci una formula chimica (es. H2SO4, NaCl, CH4): ")
    analizza_formula(formula_input)

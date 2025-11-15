from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "H0mW3HBzINpWvLxWDopaenqJI4kL2fKIMoq5eygL"
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

TRADUCCIONES = {
    "Energy": "Energía",
    "Protein": "Proteína",
    "Total lipid (fat)": "Grasas",
    "Carbohydrate, by difference": "Carbohidratos",
    "Fiber, total dietary": "Fibra",
    "Sugars, total including NLEA": "Azúcares",
    "Calcium, Ca": "Calcio",
    "Iron, Fe": "Hierro",
    "Sodium, Na": "Sodio",
    "Vitamin C, total ascorbic acid": "Vitamina C",
    "Vitamin D (D2 + D3)": "Vitamina D"
}

def traducir(nombre):
    return TRADUCCIONES.get(nombre, nombre)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/resultados", methods=["POST"])
def resultados():
    query = request.form.get("query")

    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": 1
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        return render_template("resultados.html", error="Error al conectar con la API USDA")

    data = response.json()

    if "foods" not in data or len(data["foods"]) == 0:
        return render_template("resultados.html", error="No se encontraron alimentos con ese nombre.")

    alimento = data["foods"][0]
    descripcion = alimento.get("description", "Sin descripción")

    nutrientes_crudos = alimento.get("foodNutrients", [])

    nutrientes = []
    for n in nutrientes_crudos:
        nombre = traducir(n.get("nutrientName", ""))
        valor = n.get("value", 0)
        unidad = n.get("unitName", "")
        nutrientes.append({"nombre": nombre, "valor": valor, "unidad": unidad})

    return render_template("resultados.html", description=descripcion, nutrients=nutrientes)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "clave_secreta_123"

APP_ID = "9fa1bad3"
APP_KEY = "bb57dbb4fba8dc9bfead28b22d924aea"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    alimento = request.form.get('alimento', '').strip().lower()

    if not alimento:
        flash("Por favor, ingresa un alimento para analizar.")
        return redirect(url_for('index'))

    try:
        url = (
            f"https://api.edamam.com/api/nutrition-data"
            f"?app_id={APP_ID}&app_key={APP_KEY}&ingr={alimento}"
        )
        respuesta = requests.get(url, timeout=5)

        if respuesta.status_code != 200:
            return render_template('resultados.html', error=f"Error {respuesta.status_code}: no se pudo obtener datos.")

        data = respuesta.json()
        if not data or data.get("calories", 0) == 0:
            return render_template('resultados.html', error=f"No se encontró información para '{alimento}'.")

        alimento_info = {
            "nombre": alimento,
            "calorias": data.get("calories", "N/A"),
            "peso_total": data.get("totalWeight", "N/A"),
            "nutrientes": {}
        }

        for key, val in data.get("totalNutrients", {}).items():
            alimento_info["nutrientes"][val["label"]] = round(val["quantity"], 2)

        return render_template("resultados.html", alimento=alimento_info)

    except Exception as e:
        return render_template('resultados.html', error=f"Ocurrió un error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
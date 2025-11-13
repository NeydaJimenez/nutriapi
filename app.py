from flask import Flask, render_template, request, redirect, url_for
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

APP_ID = os.getenv('EDAMAM_APP_ID')
APP_KEY = os.getenv('EDAMAM_APP_KEY')

BASE_URL = "https://api.edamam.com/api/recipes/v2"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        from_ = 0 
        to = 5     
        url = f"{BASE_URL}?type=public&q={query}&app_id={APP_ID}&app_key={APP_KEY}&from={from_}&to={to}"

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            recipes = data['hits']
            return render_template('results.html', recipes=recipes, query=query)
        else:
            error_message = "Hubo un error al obtener los datos. Intenta nuevamente."
            return render_template('index.html', error=error_message)
    return render_template('index.html')

@app.route('/results', methods=['GET'])
def results():


    if __name__ == '__main__':
        app.run(debug=True)
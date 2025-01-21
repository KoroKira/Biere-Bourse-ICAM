from flask import Flask, render_template, request, redirect, url_for
import json
import os
import random
import threading
import time

app = Flask(__name__)

DATA_FILE = 'data.json'
SHORTING_FILE = 'shorting.json'

# Fonction pour charger les données des bières
def load_data():
    if not os.path.exists(DATA_FILE):
        return [
            {"name": "IPA", "min_price": 2.0, "max_price": 8.0, "current_price": 5.0, "consumed": 0},
            {"name": "Stout", "min_price": 2.0, "max_price": 9.0, "current_price": 6.0, "consumed": 0},
            {"name": "Lager", "min_price": 2.0, "max_price": 7.0, "current_price": 4.5, "consumed": 0},
            {"name": "Pale Ale", "min_price": 2.0, "max_price": 8.5, "current_price": 5.5, "consumed": 0},
            {"name": "Pilsner", "min_price": 2.0, "max_price": 7.5, "current_price": 5.0, "consumed": 0},
            {"name": "Wheat Beer", "min_price": 2.0, "max_price": 6.0, "current_price": 4.0, "consumed": 0},
        ]
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# Fonction pour sauvegarder les données
def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

@app.route('/reset', methods=['POST'])
def reset():
    beers = load_data()
    for beer in beers:
        beer["consumed"] = 0
        beer["current_price"] = (beer["min_price"] + beer["max_price"]) / 2
    save_data(beers)
    return redirect(url_for('admin'))

@app.route('/admin')
def admin():
    beers = load_data()
    return render_template('admin.html', beers=beers)

@app.route('/client')
def client():
    beers = load_data()
    shorting_status = load_shorting_status()
    return render_template('client.html', beers=beers, shorting_status=shorting_status)

@app.route('/increase/<beer_name>', methods=['POST'])
def increase(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["consumed"] += 1
            beer["current_price"] += 0.002 * random.uniform(0, 1) * beer["current_price"]
    
    for beer in beers:
        if beer["name"] != beer_name:
            beer["current_price"] -= 0.002 * random.uniform(0, 1) * beer["current_price"]
            beer["current_price"] = max(beer["current_price"], beer["min_price"])

    save_data(beers)
    
    # Rediriger en fonction de la page d'origine
    referer = request.referrer
    if referer and 'serveur' in referer:
        return redirect(url_for('serveur'))
    return redirect(url_for('admin'))

@app.route('/decrease/<beer_name>', methods=['POST'])
def decrease(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name and beer["consumed"] > 0:
            beer["consumed"] -= 1
            beer["current_price"] -= 0.002 * random.uniform(0, 1) * beer["current_price"]
            beer["current_price"] = max(beer["current_price"], beer["min_price"])

    save_data(beers)
    return redirect(url_for('admin'))


# Fonction pour charger l'état du shorting
def load_shorting_status():
    if not os.path.exists(SHORTING_FILE):
        default_status = {"is_active": False, "end_time": 0}
        save_shorting_status(default_status)
        return default_status
    with open(SHORTING_FILE, 'r') as file:
        return json.load(file)


# Fonction pour sauvegarder l'état du shorting
def save_shorting_status(status):
    with open(SHORTING_FILE, 'w') as file:
        json.dump(status, file)

@app.route('/shorting', methods=['POST'])
def shorting():
    beers = load_data()
    for beer in beers:
        beer["current_price"] = 2.0 + 0.2 * random.uniform(0, 1)
    save_data(beers)

    shorting_status = {"is_active": True, "end_time": time.time() + 120}
    save_shorting_status(shorting_status)

    # Réinitialiser après 120 secondes
    def reset_prices():
        beers = load_data()
        for beer in beers:
            beer["current_price"] = (beer["min_price"] + beer["max_price"]) / 2
        save_data(beers)

        shorting_status["is_active"] = False
        shorting_status["end_time"] = 0
        save_shorting_status(shorting_status)

    threading.Timer(120, reset_prices).start()
    return redirect(url_for('shorting_page'))


@app.route('/shorting/increase_price/<beer_name>', methods=['POST'])
def shorting_increase_price(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["current_price"] += 1
            break
    save_data(beers)
    return redirect(url_for('shorting_page'))


@app.route('/shorting/decrease_price/<beer_name>', methods=['POST'])
def shorting_decrease_price(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["current_price"] = max(beer["current_price"] - 1, beer["min_price"])
            break
    save_data(beers)
    return redirect(url_for('shorting_page'))


@app.route('/shorting/increase_price_small/<beer_name>', methods=['POST'])
def shorting_increase_price_small(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["current_price"] += 0.1
            break
    save_data(beers)
    return redirect(url_for('shorting_page'))


@app.route('/shorting/decrease_price_small/<beer_name>', methods=['POST'])
def shorting_decrease_price_small(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["current_price"] = max(beer["current_price"] - 0.1, beer["min_price"])
            break
    save_data(beers)
    return redirect(url_for('shorting_page'))


@app.route('/shorting_page')
def shorting_page():
    beers = load_data()
    shorting_status = load_shorting_status()
    return render_template('shorting.html', beers=beers, shorting_status=shorting_status)


@app.route('/serveur')
def serveur():
    beers = load_data()
    return render_template('serveur.html', beers=beers)

@app.route('/serveur/increase/<beer_name>', methods=['POST'])
def serveur_increase(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["consumed"] += 1
            break
    save_data(beers)
    return redirect(url_for('serveur'))

COURBE_FILE = 'courbe.json'

# Fonction pour ajouter une entrée dans courbe.json
def append_to_courbe(data):
    if not os.path.exists(COURBE_FILE):
        with open(COURBE_FILE, 'w') as file:
            json.dump([], file)  # Initialise un tableau vide

    with open(COURBE_FILE, 'r+') as file:
        existing_data = json.load(file)
        existing_data.append({"timestamp": time.time(), "data": data})
        file.seek(0)
        json.dump(existing_data, file)

# Fonction pour sauvegarder les données périodiquement
def periodic_save():
    while True:
        beers = load_data()
        append_to_courbe(beers)
        time.sleep(60)  # Attend 60 secondes avant la prochaine sauvegarde

# Lancer la sauvegarde en arrière-plan
threading.Thread(target=periodic_save, daemon=True).start()

@app.route('/courbe')
def courbe():
    if not os.path.exists(COURBE_FILE):
        return render_template('courbe.html', chart_data=[])
    
    with open(COURBE_FILE, 'r') as file:
        data = json.load(file)

    # Préparer les données pour Chart.js
    chart_data = {
        "labels": [entry["timestamp"] for entry in data],
        "datasets": [
            {
                "label": beer["name"],
                "data": [entry["data"][i]["current_price"] for entry in data],
                "borderColor": f"rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 1)",
                "fill": False
            } for i, beer in enumerate(data[0]["data"])
        ]
    }

    return render_template('courbe.html', chart_data=json.dumps(chart_data))


if __name__ == '__main__':
    app.run(debug=True)


#if __name__ == '__main__':
#    app.run(debug=True, host="0.0.0.0", port=5000)

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
            {"name": "Queue Charrue", "min_price": 2.0, "max_price": 8.0, "current_price": 5.0, "consumed": 0},
            {"name": "Slash", "min_price": 2.0, "max_price": 9.0, "current_price": 6.0, "consumed": 0},
            {"name": "Bleu", "min_price": 2.0, "max_price": 7.0, "current_price": 4.5, "consumed": 0},
            {"name": "Bière des Dieux", "min_price": 2.0, "max_price": 8.5, "current_price": 5.5, "consumed": 0},
            {"name": "Rose", "min_price": 2.0, "max_price": 7.5, "current_price": 5.0, "consumed": 0},
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
    return redirect(url_for('shorting_page'))

@app.route('/admin')
def admin():
    beers = load_data()
    shorting_animation=app.config.get('SHORTING_ANIMATION', False)
    return render_template('admin.html', beers=beers)

@app.route('/client')
def client():
    beers = load_data()
    shorting_status = load_shorting_status()
    shorting_animation=app.config.get('SHORTING_ANIMATION', False)
    return render_template('client.html', beers=beers, shorting_status=shorting_status)

@app.route('/increase/<beer_name>', methods=['POST'])
def increase(beer_name):
    beers = load_data()
    for beer in beers:
        if beer["name"] == beer_name:
            beer["consumed"] += 1
            beer["current_price"] += 0.02 * random.uniform(0, 1) * beer["current_price"]
    
    for beer in beers:
        if beer["name"] != beer_name:
            beer["current_price"] -= 0.02 * random.uniform(0, 1) * beer["current_price"]
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

    # Set global shorting animation flag
    app.config['SHORTING_ANIMATION'] = True

    shorting_status = {"is_active": True, "end_time": time.time() + 120}
    save_shorting_status(shorting_status)

    def reset_prices():
        beers = load_data()
        for beer in beers:
            beer["current_price"] = (beer["min_price"] + beer["max_price"]) / 2
        save_data(beers)

        shorting_status["is_active"] = False
        shorting_status["end_time"] = 0
        save_shorting_status(shorting_status)
        
        # Clear shorting animation flag
        app.config['SHORTING_ANIMATION'] = False

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
    shorting_animation=app.config.get('SHORTING_ANIMATION', False)
    return render_template('shorting.html', beers=beers, shorting_status=shorting_status)


@app.route('/serveur')
def serveur():
    beers = load_data()
    shorting_animation=app.config.get('SHORTING_ANIMATION', False)
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

# Fonction pour ajouter des données à la courbe
def append_to_courbe(data):
    try:
        # Use a lock to prevent concurrent file access
        with threading.Lock():
            # Ensure file exists and is valid
            if not os.path.exists(COURBE_FILE):
                with open(COURBE_FILE, 'w') as file:
                    json.dump([], file)

            # Read existing data safely
            with open(COURBE_FILE, 'r+') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []

                # Append new entry
                existing_data.append({"timestamp": time.time(), "data": data})

                # Truncate file and write entire updated list
                file.seek(0)
                file.truncate()
                json.dump(existing_data, file)

    except Exception as e:
        print(f"Error in append_to_courbe: {e}")


# Fonction pour sauvegarder les données périodiquement
def periodic_save():
    while True:
        try:
            beers = load_data()
            append_to_courbe(beers)
            time.sleep(60)  # Wait 60 seconds between saves
        except Exception as e:
            print(f"Error in periodic_save: {e}")
            time.sleep(60)  # Prevent tight error loop

# Lancer la sauvegarde en arrière-plan
threading.Thread(target=periodic_save, daemon=True).start()

@app.route('/courbe')
def courbe():
    if not os.path.exists(COURBE_FILE):
        shorting_animation=app.config.get('SHORTING_ANIMATION', False)
        return render_template('courbe.html', chart_data=[])
    
    with open(COURBE_FILE, 'r') as file:
        data = json.load(file)
    
    # Neon color palette for distinct beer colors
    NEON_COLORS = [
        "rgba(255, 0, 255, 1)",    # Neon Magenta
        "rgba(0, 255, 255, 1)",    # Neon Cyan
        "rgba(255, 255, 0, 1)",    # Neon Yellow
        "rgba(0, 255, 0, 1)",      # Neon Green
        "rgba(255, 128, 0, 1)",    # Neon Orange
        "rgba(128, 0, 255, 1)"     # Neon Purple
    ]
    
    # Préparer les données pour Chart.js
    chart_data = {
        "labels": [entry["timestamp"] for entry in data],
        "datasets": [
            {
                "label": beer["name"],
                "data": [entry["data"][i]["current_price"] for entry in data],
                "borderColor": NEON_COLORS[i % len(NEON_COLORS)],
                "fill": False
            } for i, beer in enumerate(data[0]["data"])
        ]
    }
    
    return render_template('courbe.html', chart_data=json.dumps(chart_data))

@app.route('/delete_old_data')
def delete_old_data():
    try:
        if not os.path.exists(COURBE_FILE):
            return redirect(url_for('courbe'))
        
        with open(COURBE_FILE, 'r') as file:
            data = json.load(file)

        # Remove entries older than 20 minutes
        current_time = time.time()
        filtered_data = [entry for entry in data if current_time - entry["timestamp"] <= 20 * 60]

        with open(COURBE_FILE, 'w') as file:
            json.dump(filtered_data, file)

        return redirect(url_for('courbe'))
    
    except Exception as e:
        print(f"Error in delete_old_data: {e}")
        return redirect(url_for('courbe'))

def periodic_data_cleanup():
    while True:
        try:
            if os.path.exists(COURBE_FILE):
                with open(COURBE_FILE, 'r') as file:
                    data = json.load(file)

                current_time = time.time()
                filtered_data = [entry for entry in data if current_time - entry["timestamp"] <= 20 * 60]

                with open(COURBE_FILE, 'w') as file:
                    json.dump(filtered_data, file)

            time.sleep(60)  # Check and clean every minute
        except Exception as e:
            print(f"Error in periodic_data_cleanup: {e}")
            time.sleep(60)

# Add this thread alongside your periodic_save thread
threading.Thread(target=periodic_data_cleanup, daemon=True).start()


# Add a global variable to track shorting animation
app.config['SHORTING_ANIMATION'] = False

# Do the same for other routes like client, serveur, etc.

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


#if __name__ == '__main__':
#    app.run(debug=True, host="0.0.0.0", port=5000)

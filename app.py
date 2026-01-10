from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = "696163d4cc6236dae2e4086764e086cc"

# --- ZONE 1 : LES FONCTIONS OUTILS (Helpers) ---
# Il est préférable de les mettre AVANT la route principale

def get_previsions(ville, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={ville}&appid={api_key}&units=metric&lang=fr" 
    reponse = requests.get(url)
    if reponse.status_code == 200:
        data = reponse.json()
        previsions_brouillon = data['list']
        previsions = []
        for elements in previsions_brouillon:
            if "12:00:00" in elements["dt_txt"]:
                previsions_of_the_day = {
                    "date": elements['dt_txt'][:10],
                    "temp": round(elements['main']['temp']),
                    "description": elements['weather'][0]['description'],
                    "icon": elements['weather'][0]['icon']
                }
                previsions.append(previsions_of_the_day)
        return previsions
    return None

def vetement(temp, pluie):
    # ATTENTION : On utilise return, pas print !
    if temp < 10 and pluie > 0:
        return f"Il fait {temp}°C et il y a des risques de pluie. N'oubliez pas votre parapluie 😉"
    elif temp < 10 and pluie == 0:
        return f"Il fait {temp}°C, habillez-vous chaudement 😉"
    elif temp < 20 and pluie == 0:
        return f"Il fait {temp}°C, pensez à prendre une veste 😉"
    elif pluie > 0:
        return "Risque de pluie aujourd'hui. J'espère que vous n'êtes pas en sucre 😉"
    else:
        return f"Il fait {temp}°C aujourd'hui, n'oubliez pas vos lunettes de soleil 😉"

# --- ZONE 2 : LA ROUTE ---

@app.route('/', methods=['GET', 'POST'])    
def get_weather():
    ma_meteo = None
    message_erreur = None
    previ = None
    
    if request.method == "POST":
        ville_brute = request.form.get("ville_utilisateur")
        # Protection contre le vide (si l'utilisateur ne tape rien)
        if ville_brute: 
            ville = ville_brute.lower().strip()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
            reponse = requests.get(url)
            
            if reponse.status_code == 200:
                data = reponse.json()
                
                # 1. On récupère d'abord les infos de base
                temp_actuelle = round(data['main']['temp'], 1)
                pluie_actuelle = data.get('rain', {}).get('1h', 0)
                
                # 2. On appelle ta fonction conseil
                le_conseil = vetement(temp_actuelle, pluie_actuelle)
                
                ma_meteo = {
                    "ville": data["name"],
                    "temperature": temp_actuelle,
                    "description": data['weather'][0]['description'],
                    "icon": data['weather'][0]['icon'],
                    "humidite": data['main']['humidity'],
                    "vent": round(data['wind']['speed'] * 3.6),
                    "pluie": pluie_actuelle,
                    "conseil": le_conseil  # <--- On l'ajoute ici pour le HTML !
                }
                
                previ = get_previsions(ville, api_key)
            else:
                message_erreur = "Ville introuvable, vérifiez l'orthographe"
                
    return render_template("index.html", ma_meteo=ma_meteo, previsions=previ, error=message_erreur)

if __name__ == '__main__':
    app.run(debug=True)
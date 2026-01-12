from flask import Flask, render_template, request
import requests
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("OPENWEATHER_API_KEY")

print(f"Ma clé API est : {api_key}") 

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
    
def get_heure(decalage_secondes):
    temps_uct = datetime.now(timezone.utc)
    shift = timedelta(seconds=decalage_secondes)
    temps_local = temps_uct + shift
    return temps_local.strftime("%H:%M")

@app.route('/', methods=['GET', 'POST'])    
def get_weather():
    ma_meteo = None
    message_erreur = None
    previ = None
    
    if request.method == "POST":
        ville_brute = request.form.get("ville_utilisateur")
        if ville_brute: 
            ville = ville_brute.lower().strip()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
            reponse = requests.get(url)
            
            if reponse.status_code == 200:
                data = reponse.json()
                
                temp_actuelle = round(data['main']['temp'], 1)
                pluie_actuelle = data.get('rain', {}).get('1h', 0)
                
                le_conseil = vetement(temp_actuelle, pluie_actuelle)
                
                decalage = data['timezone']
                
                heure_locale = get_heure(decalage)

                ma_meteo = {
                    "ville": data["name"],
                    "temperature": temp_actuelle,
                    "heure" : heure_locale,
                    "description": data['weather'][0]['description'],
                    "icon": data['weather'][0]['icon'],
                    "humidite": data['main']['humidity'],
                    "vent": round(data['wind']['speed'] * 3.6),
                    "pluie": pluie_actuelle,
                    "conseil": le_conseil  
                }
                
                previ = get_previsions(ville, api_key)
            else:
                print(f"Erreur API : {reponse.status_code}")
                message_erreur = "Ville introuvable, vérifiez l'orthographe"
                
    return render_template("index.html", ma_meteo=ma_meteo, previsions=previ, error=message_erreur)

if __name__ == '__main__':
    app.run(debug=True)
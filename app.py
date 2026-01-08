from flask import Flask, render_template, request
import requests

app = Flask(__name__)

api_key = "696163d4cc6236dae2e4086764e086cc"
@app.route('/', methods=['GET', 'POST'])    
def get_weather():
    ma_meteo=None
    message_erreur=None
    previ = None
    if request.method == "POST":
        ville = request.form.get("ville_utilisateur")
        if ville:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
            reponse = requests.get(url)
            if reponse.status_code == 200:
                data = reponse.json()
                ma_meteo = {
                "ville": ville,
                "temperature": round(data['main']['temp']),
                "description": data['weather'][0]['description'],
                "icon": data['weather'][0]['icon'],
                "humidite": data['main']['humidity'],
                "vent": round(data['wind']['speed'] * 3.6),
                "pluie": data.get('rain', {}).get('1h', 0)
                }
                previ = get_previsions(ville, api_key)
            else:
                message_erreur = "Ville introuvable, vérifiez l'orthographe"
                
    return render_template("index.html", ma_meteo=ma_meteo, previsions = previ, error=message_erreur)

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
if __name__ == '__main__':
    app.run(debug=True)
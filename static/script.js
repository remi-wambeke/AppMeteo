function updateMeteo(element) {
    // 1. Récupération des données stockées dans la carte cliquée
    let date = element.getAttribute("data-date");
    let heure = element.getAttribute("data-heure"); // Spécifique à "Aujourd'hui"
    let temp = element.getAttribute("data-temp");
    let ressentie = element.getAttribute("data-ressentie");
    let desc = element.getAttribute("data-desc");
    let icon = element.getAttribute("data-icon");
    let hum = element.getAttribute("data-hum");
    let vent = element.getAttribute("data-vent");
    let pluie = element.getAttribute("data-pluie");
    let hasSun = element.getAttribute("data-has-sun"); // "true" ou "false"

    // 2. Gestion intelligente du TITRE (Heure ou Date)
    let spanHeure = document.getElementById("main-heure");
    // Si la carte a une heure définie (donc c'est la carte "Aujourd'hui")
    if (heure && heure !== "null" && date === "Aujourd'hui") {
        spanHeure.innerText = "(" + heure + ")";
    } else {
        // Sinon c'est une prévision
        spanHeure.innerText = "(Prévision du " + date + ")";
    }

    // 3. Mise à jour des textes et images classiques
    document.getElementById("main-temp").innerText = temp + "°C";
    document.getElementById("main-ressentie").innerText = ressentie + "°C";
    document.getElementById("main-desc").innerText = desc;
    document.getElementById("main-icon").src = "http://openweathermap.org/img/wn/" + icon + "@2x.png";
    document.getElementById("main-hum").innerText = hum;
    document.getElementById("main-vent").innerText = vent;

    // 4. Gestion de la PLUIE
    let pluieBloc = document.getElementById("bloc-pluie");
    // On vérifie si la pluie existe et si c'est un chiffre supérieur à 0
    if (pluie && parseFloat(pluie) > 0) {
        pluieBloc.style.display = "block";
        document.getElementById("main-pluie").innerText = pluie;
    } else {
        pluieBloc.style.display = "none";
    }

    // 5. Gestion du SOLEIL
    let soleilBloc = document.getElementById("bloc-soleil");
    // Sécurité : on vérifie que le bloc existe dans le HTML avant de le modifier
    if (soleilBloc) {
        if (hasSun === "true") {
            soleilBloc.style.display = "block"; // On affiche
        } else {
            soleilBloc.style.display = "none";  // On cache
        }
    }
}
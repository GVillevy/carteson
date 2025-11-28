from flask import Flask, render_template
import csv
from datetime import date
import os
import sqlite3

app = Flask(__name__)

@app.route("/test")
def home():
    return render_template("index.html")



@app.route("/")
def pepites():

    # Connexion au fichier SQLite
    conn = sqlite3.connect("../db.sqlite")
    cursor = conn.cursor()

    # Exécution de la requête
    cursor.execute("SELECT * FROM pepites WHERE running_date = (SELECT MAX(running_date) FROM pepites) ORDER BY score DESC;")
    rows = cursor.fetchall()  # récupère toutes les lignes

    # Récupérer les noms des colonnes pour construire des dictionnaires
    columns = [col[0] for col in cursor.description]

    # Préparer les listes
    artistes = []
    difference_days_list = []

    for row in rows:
        row_dict = dict(zip(columns, row))  # transforme la ligne en dict
        row_dict["difference_days"] = int(row_dict["difference_days"])  # si nécessaire
        difference_days_list.append(row_dict["difference_days"])
        artistes.append(row_dict)
        running_date = row_dict["running_date"]  # tu peux récupérer la dernière date par exemple

    conn.close()

    # Calcul moyenne
    moyenne = sum(difference_days_list) / len(difference_days_list)
    min_val = min(difference_days_list)
    max_val = max(difference_days_list)

    def value_to_color(val):
        pastel_min = 120
        darken = 0.15  # entre 0.5 et 0.9 selon l'effet voulu

        if val <= moyenne:
            ratio = (val - min_val) / (moyenne - min_val + 1e-6)
            r = int((pastel_min + (255 - pastel_min) * ratio) * darken)
            g = int(255 * darken)
        else:
            ratio = (val - moyenne) / (max_val - moyenne + 1e-6)
            r = int(255 * darken)
            g = int((pastel_min + (255 - pastel_min) * (1 - ratio)) * darken)

        b = int(pastel_min * darken)

        return f"rgb({r},{g},{b})"


    for row in artistes:
        row["color"] = value_to_color(row["difference_days"])



    return render_template("pepites.html", artistes=artistes,running_date=running_date)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit le port via cette variable
    app.run(host="0.0.0.0", port=port)
    #app.run(debug=True)

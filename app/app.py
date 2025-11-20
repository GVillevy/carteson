from flask import Flask, render_template
import csv
from datetime import date
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/pepites")
def pepites():
    
    today = date.today() 
    formatted_date = today.strftime("%d-%m-%Y")
    formatted_date = "19-11-2025"
    artistes = []
    difference_days_list = []

    # Lecture CSV
    with open("../res_trie/res_trie"+formatted_date+".csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["difference_days"] = int(row["difference_days"])
            difference_days_list.append(row["difference_days"])
            artistes.append(row)
            running_date = row["running_date"]

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



@app.route("/famous")
def famous():

    today = date.today() 
    formatted_date = today.strftime("%d-%m-%Y")
    formatted_date = "14-11-2025"
    artistes = []
    difference_days_list = []

    # Lecture CSV
    with open("../res_famous/res_famous"+formatted_date+".csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row["difference_days"] = int(row["difference_days"])
            difference_days_list.append(row["difference_days"])
            artistes.append(row)

    # Calcul moyenne
    moyenne = sum(difference_days_list) / len(difference_days_list)
    min_val = min(difference_days_list)
    max_val = max(difference_days_list)

    def value_to_color(val):
        pastel_min = 195  # plancher pastel

        if val <= moyenne:
            # ratio 0 → moyenne
            ratio = (val - min_val) / (moyenne - min_val + 1e-6)
            r = int(pastel_min + (255 - pastel_min) * ratio)  # 156 → 255
            g = 255  # vert maximum
        else:
            # ratio moyenne → max
            ratio = (val - moyenne) / (max_val - moyenne + 1e-6)
            r = 255  # rouge maximum
            g = int(pastel_min + (255 - pastel_min) * (1 - ratio))  # 255 → 156
        b = pastel_min  # fixe pour un ton pastel doux

        return f"rgb({r},{g},{b})"


    for row in artistes:
        row["color"] = value_to_color(row["difference_days"])

    return render_template("famous.html", artistes=artistes)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit le port via cette variable
    app.run(host="0.0.0.0", port=port)
    #app.run(debug=True)

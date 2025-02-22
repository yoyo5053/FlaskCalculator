from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def kalkulacka():
    vysledek = None
    if request.method == "POST":
        try:
            cislo1 = float(request.form["cislo1"])
            cislo2 = float(request.form["cislo2"])
            operace = request.form["operace"]

            if operace == "soucet":
                vysledek = cislo1 + cislo2
            elif operace == "rozdil":
                vysledek = cislo1 - cislo2
            elif operace == "soucin":
                vysledek = cislo1 * cislo2
            elif operace == "podil":
                if cislo2 == 0:
                    vysledek = "Dělení nulou není povolené."
                else:
                    vysledek = cislo1 / cislo2
        except ValueError:
            vysledek = "Neplatný vstup. Zadejte prosím čísla."

    return render_template("calculator.html", vysledek=vysledek)

if __name__ == "__main__":
    app.run(debug=True)
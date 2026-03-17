from flask import Flask, render_template, request, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_segura_123"

ARCHIVO = "datos.json"

def cargar():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return {"caja": 0, "movimientos": []}

def guardar(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        if user == "admin" and password == "1234":
            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    data = cargar()

    if request.method == "POST":
        tipo = request.form["tipo"]
        monto = float(request.form["monto"])

        if tipo == "ingreso":
            data["caja"] += monto
            data["movimientos"].append({
                "tipo": "INGRESO",
                "monto": monto,
                "fecha": str(datetime.now())
            })

        elif tipo == "egreso":
            if monto <= data["caja"]:
                data["caja"] -= monto
                data["movimientos"].append({
                    "tipo": "EGRESO",
                    "monto": monto,
                    "fecha": str(datetime.now())
                })

        guardar(data)

    return render_template("dashboard.html", caja=data["caja"], movimientos=data["movimientos"])

@app.route("/reporte")
def reporte():
    data = cargar()
    return render_template("reporte.html", movimientos=data["movimientos"])

if __name__ == "__main__":
    app.run(debug=True)
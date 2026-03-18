from flask import Flask, render_template, request, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta"

ARCHIVO = "data.json"

def cargar():
    try:
        with open(ARCHIVO, "r") as f:
            return json.load(f)
    except:
        return {"ventas": [], "deudas": {}}

def guardar(data):
    with open(ARCHIVO, "w") as f:
        json.dump(data, f, indent=4)

# -------- LOGIN --------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        if user == "admin" and password == "1234":
            session["user"] = user
            return redirect("/dashboard")

    return render_template("login.html")

# -------- DASHBOARD --------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    data = cargar()

    total_ventas = sum(v["monto"] for v in data["ventas"])
    total_deudas = sum(data["deudas"].values())

    return render_template("dashboard.html",
                           ventas=data["ventas"],
                           deudas=data["deudas"],
                           total_ventas=total_ventas,
                           total_deudas=total_deudas)

# -------- REGISTRAR VENTA --------

@app.route("/venta", methods=["POST"])
def venta():
    data = cargar()

    monto = float(request.form["monto"])
    cliente = request.form.get("cliente")

    venta = {
        "monto": monto,
        "cliente": cliente,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data["ventas"].append(venta)

    if cliente:
        data["deudas"][cliente] = data["deudas"].get(cliente, 0) + monto

    guardar(data)
    return redirect("/dashboard")

# -------- ABONO --------

@app.route("/abono", methods=["POST"])
def abono():
    data = cargar()

    cliente = request.form["cliente"]
    monto = float(request.form["monto"])

    if cliente in data["deudas"]:
        data["deudas"][cliente] -= monto

        if data["deudas"][cliente] <= 0:
            del data["deudas"][cliente]

    guardar(data)
    return redirect("/dashboard")

app.run(host="0.0.0.0", port=10000)
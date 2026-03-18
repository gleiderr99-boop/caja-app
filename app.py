from flask import Flask, render_template, request, redirect, session
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "negocio_pro"

DB = "db.json"

def load_db():
    try:
        with open(DB) as f:
            return json.load(f)
    except:
        return {"ventas": [], "productos": [], "clientes": []}

def save_db(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=4)

# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["user"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    db = load_db()
    total = sum(v["total"] for v in db["ventas"])
    
    return render_template("dashboard.html", total=total, ventas=db["ventas"])

# -------- INVENTARIO --------
@app.route("/inventario", methods=["GET","POST"])
def inventario():
    if "user" not in session:
        return redirect("/")
    
    db = load_db()
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        
        db["productos"].append({"nombre": nombre, "precio": precio})
        save_db(db)
        return redirect("/inventario")
    
    return render_template("inventario.html", productos=db["productos"])

# -------- CLIENTES --------
@app.route("/clientes", methods=["GET","POST"])
def clientes():
    if "user" not in session:
        return redirect("/")
    
    db = load_db()
    
    if request.method == "POST":
        nombre = request.form["nombre"]
        db["clientes"].append(nombre)
        save_db(db)
        return redirect("/clientes")
    
    return render_template("clientes.html", clientes=db["clientes"])

# -------- VENTAS --------
@app.route("/venta", methods=["POST"])
def venta():
    db = load_db()
    
    producto = request.form["producto"]
    cantidad = int(request.form["cantidad"])
    precio = float(request.form["precio"])
    
    total = cantidad * precio
    
    db["ventas"].append({
        "producto": producto,
        "cantidad": cantidad,
        "total": total,
        "fecha": datetime.now().strftime("%Y-%m-%d")
    })
    
    save_db(db)
    return redirect("/dashboard")

app.run(host="0.0.0.0", port=10000)0000)

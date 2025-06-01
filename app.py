# ----------------------------------------------
# Autor: Iván Alexei Gamboa Bernal
# Proyecto: Sistema de gestión de torneos deportivos
# Fecha: Mayo 2025
# Contacto: gamboabernalivanalexei@gmail.com
# Logo/texto: █▓▒░ Iván de Dev Studio ░▒▓█
# ----------------------------------------------

from flask import Flask, render_template, request, redirect, url_for
import datetime, os, hashlib

def calcular_hash_imagen():
    ruta = os.path.join("static_minified", "img", "auth_key.jpg")
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, "rb") as f:
            contenido = f.read()
            return hashlib.sha256(contenido).hexdigest()
    except Exception:
        return None

CORRECT_IMAGE_HASH = calcular_hash_imagen()

app = Flask(__name__,
            template_folder='templates_minified',
            static_folder='static_minified')

def verificar_imagen_clave():
    ruta = os.path.join("static_minified", "img", "auth_key.jpg")

    if not os.path.exists(ruta):
        return False

    try:
        with open(ruta, "rb") as f:
            contenido = f.read()
            hash_actual = hashlib.sha256(contenido).hexdigest()
    except Exception:
        return False

    if CORRECT_IMAGE_HASH is None:
        return False

    return hash_actual == CORRECT_IMAGE_HASH

@app.before_request
def bloquear_sin_imagen():
    if not verificar_imagen_clave():
        return render_template("key_error.html"), 403

USUARIOS_VALIDOS = {
    "navi@hotmail.com": "198902",
    "logan@gmail.com": "danielogan"
}

USUARIOS_ORGANIZADORES = {
    "samanta@hotmail.com": "sam123",
    "admin@hotmail.com": "1234"
}

@app.route("/", methods=["GET"])
def home():
    now = datetime.datetime.now()
    hora_actual_formato = now.strftime("%H:%M:%S")
    return render_template("index.min.html",
                           hora_actual=hora_actual_formato,
                           error=request.args.get('error'))

@app.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    if email in USUARIOS_VALIDOS and USUARIOS_VALIDOS[email] == password:
        return redirect(url_for('dashboard', user_email=email, role='usuario'))
    else:
        return redirect(url_for('home', error="Email o contraseña incorrectos."))

@app.route("/guest-mode")
def guest_mode():
    now = datetime.datetime.now()
    hora_actual_formato = now.strftime("%H:%M:%S")
    return render_template("guest_dashboard.min.html", hora_actual=hora_actual_formato)

@app.route("/organizer-login", methods=["GET"])
def organizer_login():
    now = datetime.datetime.now()
    hora_actual_formato = now.strftime("%H:%M:%S")
    return render_template("login_organizer.min.html",
                           hora_actual=hora_actual_formato,
                           error=request.args.get('error'))

@app.route("/login-organizer-process", methods=["POST"])
def login_organizer_process():
    email = request.form['email']
    password = request.form['password']
    if email in USUARIOS_ORGANIZADORES and USUARIOS_ORGANIZADORES[email] == password:
        return redirect(url_for('dashboard', user_email=email, role='organizador'))
    else:
        return redirect(url_for('organizer_login', error="Credenciales de organizador incorrectas."))

@app.route("/organizer-mode")
def organizer_mode():
    return redirect(url_for('organizer_login'))

@app.route("/dashboard")
def dashboard():
    user_email = request.args.get('user_email', 'invitado')
    user_role = request.args.get('role', 'invitado')
    return render_template("dashboard.min.html", user_email=user_email, user_role=user_role)

@app.route("/desarrolladores")
def desarrolladores():
    return render_template("desarrolladores.min.html")

if __name__ == "__main__":
    # Cambia debug a False para producción
    app.run(debug=False, port=8080, host="0.0.0.0")
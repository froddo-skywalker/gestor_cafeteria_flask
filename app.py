
from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "<h1>Gestor de Cafetería</h1><p>Servidor funcionando correctamente.</p>"

# app/__init__.py

from flask import Flask
from flask_login import LoginManager
from .auth import Usuario
from .database import get_connection

app = Flask(__name__)
app.secret_key = '2908'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    data = cursor.fetchone()
    conn.close()
    if data:
        return Usuario(data['id'], data['nombre'], data['username'], data['password_hash'])
    return None

# Importa las rutas para que se registren en la app
from . import routes



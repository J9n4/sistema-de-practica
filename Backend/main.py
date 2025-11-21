import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Cargar archivo .env
load_dotenv()

app = Flask(__name__)

# Configuración de la base de datos
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_server = os.getenv('DB_SERVER')
db_name = os.getenv('DB_NAME')
drivername = 'ODBC Driver 17 for SQL Server'

# Configuracion Flask BD
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mssql+pyodbc://{db_user}:{db_password}@"
    f"{db_server}/{db_name}?"
    f"driver={drivername.replace(' ', '+')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuracion Claves Secretas
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Importacion de modelos
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Importar modelos para crear tablas
try:
    from . import models
except ImportError:
    pass

#Rutas
@app.route('/')

def index():

    data = {
        'titulo': 'Sistema de Practica'
    }

    return render_template('index.html', data = data)

@app.route('/api/status')
def status():
    return jsonify({"estado": "Conectado","backend": "Flask"}),

def pagina_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    
    #Crear tablas si no existen
    with app.app_context():
        db.create_all()
        print("Base de datos conectada y tablas creadas")

    app.register_error_handler(404, pagina_error)
    app.run(debug=True, port= 5000)
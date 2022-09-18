from flask import Flask, render_template,request,session
from flask_bootstrap import Bootstrap
from basededatos import iniciar_bd, db
#from modelos import Eventos, Categorias
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy.sql.expression import func
from os import getenv
import os
app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
cadenapsql = getenv('DATABASEURI')
app.config['SQLALCHEMY_DATABASE_URI'] = cadenapsql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = './static/images/'
engine = iniciar_bd(app, cadenapsql)

Bootstrap(app)
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro_p')
def registro_p():
    return render_template('registro_Peliculas.html')

if __name__ == '__main__':
    app.run(debug=True)
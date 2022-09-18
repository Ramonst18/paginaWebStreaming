from flask import Flask, render_template,request,session
from flask_bootstrap import Bootstrap
from basededatos import crear_bd, iniciar_bd, db
from modelos import Eventos, Categorias
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy.sql.expression import func
from os import getenv

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro_p')
def registro_p():
    return render_template('registro_Peliculas.html')

if __name__ == '__main__':
    app.run(debug=True)
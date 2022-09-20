from flask import Flask, render_template,request,session
from flask_bootstrap import Bootstrap
from basededatos import iniciar_bd, db, crear_bd
from tablas import Peliculas
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
crear_bd(app, engine)
Bootstrap(app)

###### Para realizar la solicitud de informacion de alguna de las tablas se debera de poner lo siguiente
# Resultado = db.session.query("Nombre de la tabla, inicial mayuscula y sin comillas").all()
# Ejemplo: peliculasResultado = db.session.query(Peliculas).all()


@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro_p', methods=["GET", "POST"])
def registro_p():
    #realizamos las consultas y guardamos en una variable
    peliculasResultado = db.session.query(Peliculas).all()
    
    if request.method == 'POST':
        # Obtenemos todos los atributos y las almacenamos en variables
        titulo = request.form["Titulo"]
        anio = int(request.form["Anio"])
        director = request.form["Director"]
        genero = request.form["Genero"]
        duracion = int(request.form["Duracion"])
        elenco = request.form["Elenco"]
        clasificacion_IMBD = float(request.form["CIMDB"])
        pais = request.form["Pais"]
        clasificacion_edad = request.form["Cedad"]
        sinopsis = request.form["Sinopsis"]
        Tcontenido = request.form["Tcontenido"]
        
        #Para guardar la imagen del poster
        poster = request.files["Poster"]
        poster_nombre = poster.filename
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], poster_nombre))
        
        #Creamos la clase y guardamos la informacion en la base de datos
        peliculas = Peliculas(titulo, anio, director, genero, duracion, elenco, clasificacion_IMBD, pais, clasificacion_edad, sinopsis, poster_nombre, Tcontenido)
        
        db.session.add(peliculas)
        db.session.commit()
        peliculasResultado = db.session.query(Peliculas).all()
        print(peliculasResultado)
        return render_template('registro_Peliculas.html')
    return render_template('registro_Peliculas.html')

if __name__ == '__main__':
    app.run(debug=True)
from datetime import date
from Database import Database
from flask import Flask, render_template, request, session
from flask_bootstrap import Bootstrap
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect
import json
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = './static/images/posters/' # Folder donde se guardaran los posters
Bootstrap(app)

bd = Database() # Objeto correspondiente a la BD

'''
    SOBRE LA REALIZACIÓN DE QUERIES:
    > Query regresa resultado (SELECT)?
        resultado = db.execute_query_return(sql:str)
    > Query no regresa resultado (INSERT,UPDATE,DELETE)?
        db.execute_query(sql:str)
'''

# Página donde se mostrará el inicio del servicio, aqui se mostrará los botones de inicio de sesion
# O de registro de usuario, despues de darle a uno se redireccionará a la pagina de inicio de sesion 
# O de registro
@app.route('/')
def inicio():
    return render_template('inicio.html')

# Módulo de registro de películas (Sólo accesible para admin)
# NECESITA VALIDACIÓN DE INICIO DE SESIÓN
@app.route('/registro_peliculas', methods=["GET", "POST"])
def registro_peliculas():
    if request.method == 'POST':
        # Obtenemos todos los atributos y las almacenamos en variables
        titulo = request.form["Titulo"]
        año = int(request.form["Año"])
        director = request.form["Director"]
        genero = request.form["Genero"]
        duracion = int(request.form["Duracion"])
        elenco = request.form["Elenco"]
        calif_IMBD = float(request.form["CIMDB"])
        pais = request.form["Pais"]
        clasificacion_edad = request.form["CEdad"]
        sinopsis = request.form["Sinopsis"]
        
        #Para guardar la imagen del poster
        poster = request.files["Poster"]
        poster_nombre = poster.filename
        poster.save(os.path.join(UPLOAD_FOLDER, poster_nombre))
        
        stream_video = request.form["StreamVideo"]
        fecha_agregada = str(date.today())
        tipo_contenido = request.form["TContenido"]
        
        
        # Preparar el SQL statement
        sql = ("INSERT INTO Peliculas(titulo,año,director,genero,duracion,elenco,calif_imbd,pais,clasif_por_edad,sinopsis,poster,stream_video,fecha_agregada,visualizaciones,tipo_contenido)"
           "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}');").format(
               titulo,año,director,genero,duracion,elenco,calif_IMBD,pais,clasificacion_edad,sinopsis,
               poster_nombre,stream_video,fecha_agregada,0,tipo_contenido
           )

        bd.execute_query(sql) # Realizar la consulta
 
    return render_template('registro_peliculas.html')

# Pagina donde se mostrará las peliculas y las opciones de administrador en el caso de que 
# la persona sea admin
#@app.route('/principal')
#def principal():

# Modulo de registro de usuarios
@app.route('/registro')
def registro_usuarios():
    return render_template('registrarse.html')    

# Modulo de cuenta del usuario
# Aqui se podra actualizar los datos del cliente
@app.route('/mi_cuenta')
def cuenta():
    return render_template('mi_cuenta.html')

if __name__ == '__main__':
    app.run(debug=True)

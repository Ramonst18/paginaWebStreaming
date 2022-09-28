from datetime import date
from Database import Database
from flask import Flask, render_template, request, session
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect
from Cliente import Cliente
import json
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
UPLOAD_FOLDER = './static/images/posters/' # Folder donde se guardaran los posters

bd = Database() # Objeto correspondiente a la BD

'''
    SOBRE LA REALIZACIÓN DE QUERIES:
    > Query regresa resultado (SELECT)?
        resultado = db.execute_query_return(sql:str)
    > Query no regresa resultado (INSERT,UPDATE,DELETE)?
        db.execute_query(sql:str)
'''

# Página principal del sitio web
@app.route('/')
def index():
    if 'email' in session:
        #login = True
        # redirect comentado hatsa implementar catalogo.html
        redirect('/catalogo.html')
    else:
        # Cuando el usuario no ha iniciado sesión           
        return render_template('index.html')

# Módulo login cliente
@app.route('/login', methods=["GET", "POST"])
def login_cliente():
    if request.method == 'POST':
        email = request.form['email']
        #print(cliente.nombre + " " + cliente.ap_paterno + " " + cliente.ap_materno)
        if email_registrado(email):
            #print(email)
            cliente = obtener_cliente(email)
            if (sha256_crypt.verify(request.form['password'],cliente.contraseña) == True):   
                session['email'] = email
                return redirect('/')
            else:
                return render_template('login.html', error='Password incorrecto')
        else:
                return render_template('login.html', error='E-mail incorrecto')
    else:   
        return render_template('login.html', error=None)
# Módulo login admin

# Módulo logout

# Módulo registro de clientes

# Módulo de navegar catálogo
@app.route('/catalogo.html', methods=["GET", "POST"])
def ver_catalogo():
    usuario = None
    if 'email' in session:
        usuario = session.get('email')
    return render_template('catalogo.html', user=usuario)

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

### Metodos
# Método que valida si un email ya está registrado en la BD
def email_registrado(email:str) -> bool:
    sql = "SELECT COUNT(id_cliente) FROM Clientes WHERE email='{0}';".format(email)
    res = bd.execute_query_return(sql)
    return res[0][0] == 1

# Método para buscar en la BD al cliente con el email dado en el formulario de inicio de sesión
def obtener_cliente(email:str) -> Cliente:
    sql = "SELECT row_to_json(cliente) FROM (SELECT * FROM Clientes WHERE email='{0}') AS cliente;".format(email)
    res = bd.execute_query_return(sql)
    cliente_dict = res[0][0]
    cliente = Cliente(**cliente_dict)
    return cliente

if __name__ == '__main__':
    app.run(debug=True)

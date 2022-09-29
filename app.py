from datetime import date
from Administrador import Administrador
from Database import Database
from flask import Flask, render_template, request, session
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect
from Cliente import Cliente
import json
import os
import secrets

# Configuración de la app
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
    # Cuando el cliente ha iniciado sesión
    if 'email' in session:
        redirect('/catalogo')
    # Cuando el admin ha iniciado sesión
    elif 'ID_admin' in session:
        return render_template('registro_peliculas')
    else:
        # Cuando el usuario no ha iniciado sesión           
        return render_template('index.html')


# Módulo login cliente
@app.route('/login', methods=["GET", "POST"])
def login_cliente():
    if request.method == 'POST':
        email = request.form['email']
        if email_registrado(email):
            cliente = obtener_cliente(email)
            print(cliente.nombre)
            if (sha256_crypt.verify(request.form['password'],cliente.contraseña) == True):   
                session['email'] = email
                return redirect('/catalogo')
            else:
                return render_template('login.html', error='Contraseña incorrecta')
        else:
                return render_template('login.html', error='E-mail incorrecto')
    else:   
        return render_template('login.html', error=None)


# Módulo login admin
@app.route('/admin_login', methods=["GET", "POST"])
def login_admin():
    if request.method == 'POST':
        ID_admin = request.form['ID']
        if ID_registrado(ID_admin):
            admin = obtener_admin(ID_admin)
            if (sha256_crypt.verify(request.form['password'],admin.contraseña) == True):   
                session['ID_admin'] = ID_admin
                return redirect('/registro_peliculas')
            else:
                return render_template('login.html', error='Contraseña incorrecta')
        else:
                return render_template('login.html', error='ID incorrecto')
    else:   
        return render_template('login.html', error=None)


# Módulo Logout
@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        return redirect('/')
    elif 'ID_admin' in session:
        session.pop('ID_admin', None)
        return redirect('/')


# Módulo registro de clientes
@app.route('/registro',methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        if not email_registrado(request.form['email']):
            if request.form['contraseña'] == request.form['confirmar_contraseña']:
                registrar_cliente(request.form.to_dict()) # Usar formulario convertido en diccionario como parámetro
                session['email'] = request.form['email']
                return redirect('/')
            else:
                return render_template('registro.html',error="Las contraseñas no coinciden. Inténtelo de nuevo.")
        else:
            return render_template('registro.html',error="El correo electrónico ya está registrado.")
    else:
        return render_template('registro.html',error=None)

# Módulo registro de administradores
@app.route('/registro_admin',methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        if not id_registrado(request.form['id']):
            if request.form['contraseña'] == request.form['confirmar_contraseña']:
                registrar_cliente(request.form.to_dict()) # Usar formulario convertido en diccionario como parámetro
                session['id'] = request.form['id']
                return redirect('/')
            else:
                return render_template('registro_admin.html',error="Las contraseñas no coinciden. Inténtelo de nuevo.")
        else:
            return render_template('registro_admin.html',error="El ID ya está registrado.")
    else:
        return render_template('registro_admin.html',error=None)

# Módulo de navegar catálogo
@app.route('/catalogo', methods=["GET", "POST"])
def ver_catalogo():
    if 'email' in session:
        usuario = session.get('email')
        return render_template('catalogo.html', user=usuario)
    else:
        return render_template('catalogo.html', user=None)


# Módulo de registro de películas (Sólo accesible para admin)
@app.route('/registro_peliculas', methods=["GET", "POST"])
def registro_peliculas():
    if 'ID_admin' in session:
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
#@app.route('/admin_index')
#def admin_index():
   


# Modulo de cuenta del usuario
# Aqui se podra actualizar los datos del cliente
#@app.route('/mi_cuenta')
#def cuenta():
#    return render_template('mi_cuenta.html')


### MÉTODOS PARA LOGIN Y REGISTRO
# Método que valida si un email ya está registrado en la BD
def email_registrado(email:str) -> bool:
    sql = "SELECT COUNT(id_cliente) FROM Clientes WHERE email='{0}';".format(email)
    res = bd.execute_query_return(sql)
    #print("email_registrado -> ", type(res))
    return res[0][0] == 1

# Método que valida si un ID ya está registrado en la BD
def id_registrado(id:str) -> bool:
    sql = "SELECT COUNT(id_admin) FROM administradores WHERE id_admin='{0}';".format(id)
    res = bd.execute_query_return(sql)
    #print("email_registrado -> ", type(res))
    return res[0][0] == 1

# Método que registra en la BD un nuevo cliente con los datos del formulario
def registrar_cliente(formulario_registro:dict) -> None:
    sql = ("INSERT INTO Clientes(nombre, apellido_paterno, apellido_materno, email, contraseña, telefono)"
           "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');").format(
               formulario_registro['nombre'],
               formulario_registro['apellido_paterno'],
               formulario_registro['apellido_materno'],
               formulario_registro['email'],
               sha256_crypt.hash(formulario_registro['contraseña']),
               formulario_registro['telefono'],
           )
           
    bd.execute_query(sql)

# Método que registra en la BD un nuevo administrador con los datos del formulario
def registrar_cliente(formulario_registro:dict) -> None:
    sql = ("INSERT INTO administradores(id_admin, nombre, apellido_paterno, apellido_materno, contraseña)"
           "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');").format(
               formulario_registro['id'],
               formulario_registro['nombre'],
               formulario_registro['apellido_paterno'],
               formulario_registro['apellido_materno'],
               sha256_crypt.hash(formulario_registro['contraseña']),
           )
           
    bd.execute_query(sql)

# Método para buscar en la BD al cliente con el email dado en el formulario de inicio de sesión
def obtener_cliente(email:str) -> Cliente:
    sql = "SELECT row_to_json(cliente) FROM (SELECT * FROM Clientes WHERE email='{0}') AS cliente;".format(email)
    res = bd.execute_query_return(sql)
    cliente_dict = res[0][0]
    cliente = Cliente(**cliente_dict)
    #print("tras login cliente -> ", type(cliente))
    return cliente


# Método que valida si un ID ya está registrado en la BD
def ID_registrado(ID:int) -> bool:
    sql = "SELECT COUNT(id_admin) FROM Administradores WHERE id_admin='{0}';".format(ID)
    res = bd.execute_query_return(sql)
    #print("ID_registrado -> ", type(res))
    return res[0][0] == 1


# Metodo para buscar en la bd al admin con la ID dada por el formulario de inicio de sesion 
def obtener_admin(ID:int) -> Administrador:
    sql = "SELECT row_to_json(ID) FROM(SELECT * FROM Administradores WHERE id_admin='{0}') AS id_admin;".format(ID)
    res = bd.execute_query_return(sql)
    administrador_dict = res[0][0]
    admin = Administrador(**administrador_dict)
    #print("tras login admin -> ", type(admin))
    return admin 

if __name__ == '__main__':
    app.run(debug=True)

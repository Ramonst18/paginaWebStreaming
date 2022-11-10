from Administrador import Administrador
from Cliente import Cliente
from Database import Database
from datetime import date, datetime
from flask import Flask, render_template, request, session
from passlib.hash import sha256_crypt
from Pelicula import Pelicula
from werkzeug.utils import redirect

import os
import random
import secrets

# Configuración de la app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


# Folder donde se guardaran los posters
UPLOAD_FOLDER = './static/images/posters/'

bd = Database()  # Objeto correspondiente a la BD

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
        # Faltaba asignar return, por eso saltaba TypeError :p
        return redirect('catalogo')
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
            if (sha256_crypt.verify(request.form['password'], cliente.contraseña) == True):
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
        if id_registrado(ID_admin):
            admin = obtener_admin(ID_admin)
            if (sha256_crypt.verify(request.form['password'], admin.contraseña) == True):
                session['ID_admin'] = ID_admin
                return redirect('/registro_peliculas')
            else:
                return render_template('admin_login.html', error='Contraseña incorrecta')
        else:
            return render_template('admin_login.html', error='ID incorrecto')
    else:
        return render_template('admin_login.html', error=None)


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
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        if not email_registrado(request.form['email']):
            if request.form['contraseña'] == request.form['confirmar_contraseña']:
                # Usar formulario convertido en diccionario como parámetro
                registrar_cliente(request.form.to_dict())
                session['email'] = request.form['email']
                return redirect('/catalogo')
            else:
                return render_template('registro.html', error="Las contraseñas no coinciden. Inténtelo de nuevo.")
        else:
            return render_template('registro.html', error="El correo electrónico ya está registrado.")
    else:
        return render_template('registro.html', error=None)


# Módulo registro de administradores
@app.route('/registro_admin', methods=['GET', 'POST'])
def registro_admin():
    if request.method == 'POST':
        if not id_registrado(request.form['id_admin']):
            if request.form['contraseña'] == request.form['confirmar_contraseña']:
                # Usar formulario convertido en diccionario como parámetro
                registrar_admin(request.form.to_dict())
                session['ID_admin'] = request.form['id_admin']
                # Redirect provisional hasta tener la homepage del admin
                return redirect('/catalogo')
            else:
                return render_template('registro_admin.html', error="Las contraseñas no coinciden. Inténtelo de nuevo.")
        else:
            return render_template('registro_admin.html', error="El ID ya está registrado.")
    else:
        return render_template('registro_admin.html', error=None)


# Módulo de navegar catálogo. Funciona como página de inicio
@app.route('/catalogo', methods=["GET", "POST"])
def ver_catalogo():
    if request.method == 'POST':
        titulo = request.form['termino_busqueda']
        url = ("/buscar/{0}").format(titulo)
        return redirect(url)
    else:
        lista_top_pelis = obtener_top_pelis()
        lista_pelis_recientes = obtener_agregadas_recientemente()
        lista_recomendadas = obtener_lista_recomendaciones()
        if 'email' in session:
            usuario = session.get('email')
            return render_template('catalogo.html', user=usuario, listaTop10=lista_top_pelis, listaRecientes=lista_pelis_recientes, listaRecomendaciones=lista_recomendadas)
        else:
            return render_template('catalogo.html', user=None, listaTop10=lista_top_pelis, listaRecientes=lista_pelis_recientes, listaRecomendaciones=lista_recomendadas)
    

# Módulo para explorar películas por género
@app.route('/explorar/<genero>', methods=["GET", "POST"])
def explorar_genero(genero):
    if request.method == 'POST':
        titulo = request.form['termino_busqueda']
        url = ("/buscar/{0}").format(titulo)
        return redirect(url)
    else:
        lista_peliculas = buscar_por_genero(genero)
        if 'email' in session:
            usuario = session.get('email')
            return render_template('explorar_genero.html', user=usuario, genero=genero, listaPeliculas=lista_peliculas)
        else:
            return render_template('explorar_genero.html', user=None, genero=genero, listaPeliculas=lista_peliculas)


# Módulo para mostrar los resultados de la búsqueda por título
@app.route('/buscar/<titulo>', methods=["GET", "POST"])
def buscar_pelicula(titulo):
    if request.method == 'POST':
        titulo = request.form['termino_busqueda']
        url = ("/buscar/{0}").format(titulo)
        return redirect(url)
    else:
        lista_peliculas = buscar_por_titulo(titulo)
        if 'email' in session:
            usuario = session.get('email')
            return render_template('buscar_pelicula.html', user=usuario, titulo_busqueda=titulo, listaPeliculas=lista_peliculas)
        else:
            return render_template('buscar_pelicula.html', user=None, titulo_busqueda=titulo, listaPeliculas=lista_peliculas)


# Módulo para ver la ficha de una película
@app.route('/ver/<id_pelicula>', methods=["GET","POST"])
def vista_pelicula(id_pelicula):
    if request.method == 'POST':
        titulo = request.form['termino_busqueda']
        url = ("/buscar/{0}").format(titulo)
        return redirect(url)
    else:
        pelicula = obtener_pelicula(id_pelicula)
        if 'email' in session:
            usuario = session.get('email')
            return render_template('pelicula.html', user=usuario, pelicula=pelicula)
        else:
            return render_template('pelicula.html', user=None, pelicula=pelicula)


# Modulo de suscripcion. Aqui se podra contratar la suscripción
@app.route('/suscripcion', methods=["GET", "POST"])
def suscripcion():
    if request.method == 'POST':
        # Obtenemos los datos de la suscripcion
        #numeroTarjeta = request.form["inputNumero"]
        #nombreTarjeta = request.form["inputNombre"]
        #mesTarjeta = request.form["mes"]
        #yearTarjeta = request.form["year"]
        #ccvTarjeta = request.form["inputCCV"]
        meses = request.form["meses"]
        plan = request.form["plan"]
        plan_id = 0
        now = datetime.now()

        # verificamos el tipo de plan y establecemos el id
        if (plan == 'Basico'):
            plan_id = 1
        elif (plan == 'Plus'):
            plan_id = 2
        else:
            plan_id = 3

        fechaActual = f"{now.day}/{now.month}/{now.year}"
        fechaExpiracion = fecha_expiracion(meses)

        # Realizamos el registro
        registrar_suscripcion(fechaActual, fechaExpiracion, obtener_cliente(
            session["email"]).id_cliente, plan_id)

        # Aqui obtendremos los meses de suscripcion y el tiempo lo guardaremos en la tabla de suscripcion
        return render_template('catalogo.html')
    else:
        return render_template('suscripcion.html')


# Modulo de cuenta del usuario
# Aqui se podra actualizar los datos del cliente
@app.route('/mi_cuenta', methods=["GET", "POST"])
def cuenta():
    if request.method == 'POST':
        if 'email' in session:
            actualizar_datos_cliente(request.form.to_dict(), session['email'])

            suscripcion = obtener_suscripcion(
                obtener_id_cliente(session["email"]))

            # atualizamos el email de sesion
            session['email'] = request.form['email']
            return render_template('mi_cuenta.html', cliente=obtener_cliente(session['email']), suscripcion=suscripcion)
        elif 'ID_admin' in session:
            actualizar_datos_admin(request.form.to_dict(), session['ID_admin'])

            return render_template('mi_cuenta.html', admin=obtener_admin(session['ID_admin']))
    else:
        if 'email' in session:

            suscripcion = obtener_suscripcion(
                obtener_id_cliente(session["email"]))

            # Mandamos la informacion del cliente a la pagina de mi cuenta
            return render_template('mi_cuenta.html', cliente=obtener_cliente(session['email']), suscripcion=suscripcion)
        elif 'ID_admin' in session:
            # Mandamos la informacion del administrador a la pagina de mi cuenta
            return render_template('mi_cuenta.html', admin=obtener_admin(session['ID_admin']))


# Modulo de contacto con la empresa
@app.route('/contactar', methods=["GET", "POST"])
def contactar():
    if request.method == 'POST':
        if 'c_nombre' in request.form:
            registrar_contacto(request.form.to_dict())
            return redirect('/contactar')
        elif 'termino_busqueda' in request.form:
            titulo = request.form['termino_busqueda']
            url = ("/buscar/{0}").format(titulo)
            return redirect(url)
    else:
        if 'email' in session:
            usuario = session.get['email']
            return render_template('contactar.html', user=usuario)
        else:
            return render_template('contactar.html', user=None)


# Pagina donde se mostrará las peliculas y las opciones de administrador en el caso de que
# la persona sea admin
# @app.route('/admin_index')
# def admin_index():


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

            # Para guardar la imagen del poster
            poster = request.files["Poster"]
            poster_nombre = poster.filename
            poster.save(os.path.join(UPLOAD_FOLDER, poster_nombre))

            stream_video = request.form["StreamVideo"]
            fecha_agregada = str(date.today())
            tipo_contenido = request.form["TContenido"]

            # Preparar el SQL statement
            sql = ("INSERT INTO Peliculas(titulo,año,director,genero,duracion,elenco,calif_imbd,pais,clasif_por_edad,sinopsis,poster,stream_video,fecha_agregada,visualizaciones,tipo_contenido)"
                   "VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}', '{12}', '{13}', '{14}');").format(
                titulo, año, director, genero, duracion, elenco, calif_IMBD, pais, clasificacion_edad, sinopsis,
                poster_nombre, stream_video, fecha_agregada, 0, tipo_contenido
            )

            bd.execute_query(sql)  # Realizar la consulta

        return render_template('registro_peliculas.html')


# MÉTODOS PARA LOGIN, REGISTRO y GESTIÓN DE CUENTA
# Método que valida si un email ya está registrado en la BD
def email_registrado(email: str) -> bool:
    sql = "SELECT COUNT(id_cliente) FROM Clientes WHERE email='{0}';".format(
        email)
    res = bd.execute_query_return(sql)
    return res[0][0] == 1


def obtener_id_cliente(email):
    sql = "SELECT id_cliente FROM Clientes WHERE email='{0}';".format(email)
    res = bd.execute_query_return(sql)
    return res[0][0]


def obtener_suscripcion(id_cliente):
    sql = "SELECT * FROM suscripciones WHERE cliente_id='{0}';".format(
        id_cliente)
    res = bd.execute_query_return(sql)
    try:
        suscripcion = {
            "vencimiento": res[0][3]
        }
    except:
        suscripcion = {}
    return suscripcion


def registrar_suscripcion(fechaActual, fechaExpiracion, cliente_id, plan_id):
    sql = ("INSERT INTO suscripciones(cliente_id, plan_id, fecha_contratación, fecha_vencimiento) "
           "VALUES('{0}', '{1}', '{2}', '{3}');").format(
               cliente_id,
               plan_id,
               fechaActual,
               fechaExpiracion,
    )

    bd.execute_query(sql)


# Método que nos regresará la fecha en la cual se terminará la suscripcion
def fecha_expiracion(meses):
    """Se tiene que pasar el string de los meses que se toma de la pagina y la funcion
    regresará la fecha en cual se expire la suscripcion"""

    # tomamos los meses
    listaMeses = meses.split(' ')
    tiempoMeses = int(listaMeses[0])
    now = datetime.now()
    anio = now.year
    mes = now.month + tiempoMeses
    fechaExpiracion = f""
    print(mes)

    # verificamos el numero de meses y si es necesario cambiamos el año
    if (mes > 12):
        anio += 1
        mes -= 12

    # verificamos el tiempo en dias y si es necesario cambiamos el dia al ultimo dia del mes
    # Meses con 28 dias
    if (mes == 2):
        # verificamos el dia que no sobrepase
        if(now.day > 28):
            # creamos el string de la fecha
            fechaExpiracion = f"28/{mes}/{anio}"
    elif (mes == 4 or mes == 6 or mes == 9 or mes == 11):
        # verificamos el dia que no sobrepase
        if(now.day > 30):
            # creamos el string de la fecha
            fechaExpiracion = f"30/{mes}/{anio}"
    else:
        # creamos el string de la fecha
        fechaExpiracion = f"{now.day}/{mes}/{anio}"

    return fechaExpiracion


# Metodo que registra la informacion de la persona que se quiere contactar con la empresa
def registrar_contacto(formulario_contacto: dict):
    sql = ("INSERT INTO Contacto(nombre, correo, telefono, mensaje)"
           "VALUES('{0}', '{1}', '{2}', '{3}');").format(
               formulario_contacto['c_nombre'],
               formulario_contacto['c_correo'],
               formulario_contacto['c_telefono'],
               formulario_contacto['c_mensaje'],

    )

    bd.execute_query(sql)


# Método que registra en la BD un nuevo cliente con los datos del formulario
def registrar_cliente(formulario_registro: dict) -> None:
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


# Método para buscar en la BD al cliente con el email dado en el formulario de inicio de sesión
def obtener_cliente(email: str) -> Cliente:
    sql = "SELECT row_to_json(cliente) FROM (SELECT * FROM Clientes WHERE email='{0}') AS cliente;".format(
        email)
    res = bd.execute_query_return(sql)
    cliente_dict = res[0][0]
    cliente = Cliente(**cliente_dict)
    return cliente


# Método que valida si un ID ya está registrado en la BD
def id_registrado(ID: int) -> bool:
    sql = "SELECT COUNT(id_admin) FROM Administradores WHERE id_admin='{0}';".format(
        ID)
    res = bd.execute_query_return(sql)
    return res[0][0] == 1


# Método que registra en la BD un nuevo administrador con los datos del formulario
def registrar_admin(formulario_registro: dict) -> None:
    sql = ("INSERT INTO Administradores(id_admin, nombre, apellido_paterno, apellido_materno, contraseña)"
           "VALUES('{0}', '{1}', '{2}', '{3}', '{4}');").format(
               formulario_registro['id_admin'],
               formulario_registro['nombre'],
               formulario_registro['apellido_paterno'],
               formulario_registro['apellido_materno'],
               sha256_crypt.hash(formulario_registro['contraseña']),
    )

    bd.execute_query(sql)


# Metodo para buscar en la bd al admin con la ID dada por el formulario de inicio de sesion
def obtener_admin(ID: int) -> Administrador:
    sql = "SELECT row_to_json(administrador) FROM (SELECT * FROM Administradores WHERE id_admin='{0}') AS administrador;".format(
        ID)
    res = bd.execute_query_return(sql)
    administrador_dict = res[0][0]
    admin = Administrador(**administrador_dict)
    return admin


# Método para actualizar los datos del cliente
def actualizar_datos_cliente(formulario_usuario: dict, email):
    sql = ("UPDATE Clientes SET "
           "nombre='{0}',"
           "apellido_paterno='{1}',"
           "apellido_materno='{2}',"
           "email='{3}',"
           "telefono='{4}'"
           " WHERE email='" + email + "';").format(
               formulario_usuario['nombre'],
               formulario_usuario['apellido_paterno'],
               formulario_usuario['apellido_materno'],
               formulario_usuario['email'],
               formulario_usuario['telefono'],
    )

    bd.execute_query(sql)


# Método para actualizar los datos del administrador
def actualizar_datos_admin(formulario_admin: dict, id_admin):
    sql = ("UPDATE Administradores SET "
           "nombre='{0}',"
           "apellido_paterno='{1}',"
           "apellido_materno='{2}'"
           " WHERE id_admin='" + id_admin + "';").format(
               formulario_admin['nombre'],
               formulario_admin['apellido_paterno'],
               formulario_admin['apellido_materno'],
    )

    bd.execute_query(sql)


# MÉTODOS USADOS PARA NAVEGAR EL CATÁLOGO
def obtener_pelicula(id) -> Pelicula:
    sql = "SELECT row_to_json(pelicula) FROM (SELECT * FROM Peliculas WHERE id_pelicula = {0}) AS pelicula;".format(id)
    
    res = bd.execute_query_return(sql)
    
    pelicula = Pelicula(**res[0][0])
    
    return pelicula


# Método para obtener una lista con las 10 películas más vistas
def obtener_top_pelis() -> list['Pelicula']:
    sql = "SELECT json_agg(peliculas) FROM (SELECT * FROM Peliculas ORDER BY visualizaciones DESC LIMIT 10) AS peliculas;"
    res = bd.execute_query_return(sql)
    peliculas = res[0][0]  # Lista de diccionarios. Cada dict es una película
    # Crear una lista de objetos de la clase Película con el resultado de la query
    lista_top = [Pelicula(**p) for p in peliculas]
    return lista_top


# Método para obtener una lista de las 20 agregadas más recientemente
def obtener_agregadas_recientemente() -> list('Pelicula'):
    sql = "SELECT json_agg(peliculas) FROM (SELECT * FROM Peliculas ORDER BY fecha_agregada ASC LIMIT 20) AS peliculas;"
    res = bd.execute_query_return(sql)
    peliculas = res[0][0]  # Lista de diccionarios. Cada dict es una película
    # Crear una lista de objetos de la clase Película con el reaultado de la query
    lista_recientes = [Pelicula(**p) for p in peliculas]
    return lista_recientes


# Método para obtener una lista de 20 películas seleccionadas aleatoriamente
def obtener_lista_recomendaciones() -> list('Pelicula'):
    # Obtener el total de películas registradas
    sql_count = "SELECT COUNT(*) FROM Peliculas;"
    res_count = bd.execute_query_return(sql_count)
    # El total se usará para generar un número random
    total = res_count[0][0]

    # Generar un int random en el rango de 1 al total de peliculas menos 20.
    # De esta forma aseguramos obtener 20 resultados.
    index = random.randint(1, (total-20))

    # Obtener las 20 primeras películas con un ID mayor al index obtenido
    sql_pelis = "SELECT json_agg(peliculas) FROM (SELECT * FROM Peliculas WHERE id_pelicula >= {0}) AS peliculas;".format(
        index)

    res_pelis = bd.execute_query_return(sql_pelis)

    # Lista de diccionarios. Cada dict es una película
    peliculas = res_pelis[0][0]
    lista_recomendaciones = [Pelicula(**p) for p in peliculas]

    return lista_recomendaciones


# Método para obtener una lista las películas del género seleccionado
def buscar_por_genero(genero:str) -> list('Pelicula'):
    sql = "SELECT json_agg(peliculas) FROM (SELECT * FROM Peliculas WHERE position('{0}' in genero)>0) AS peliculas;".format(
        genero)
    
    res = bd.execute_query_return(sql)

    # Lista de diccionarios. Cada dict es una película
    peliculas = res[0][0]
    lista_peliculas = [Pelicula(**p) for p in peliculas]

    return lista_peliculas


# Método para buscar películas por título
def buscar_por_titulo(titulo:str) -> list('Pelicula'):
    sql = "SELECT json_agg(peliculas) FROM (SELECT * FROM Peliculas WHERE position(LOWER('{0}') in LOWER(titulo))>0) AS peliculas;".format(
        titulo)
    
    res = bd.execute_query_return(sql)
    
    # Lista de diccionarios. Cada dict es una pelicula
    peliculas = res[0][0]
    if peliculas == None:
        return None
    else:
        lista_peliculas = [Pelicula(**p) for p in peliculas]
        return lista_peliculas


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template,request,session
app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registro_p')
def registro_p():
    return render_template('registroPeliculas.html')

if __name__ == '__main__':
    app.run(debug=True)
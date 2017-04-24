from flask import Flask, render_template, request, url_for, redirect
from passlib.handlers.sha2_crypt import sha256_crypt
import psycopg2, time

hostname = 'localhost'
username = 'postgres'
password = 'admin'
database = 'PongGame'

myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )

myConnection.close()
conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%i'" \
              % (hostname, database, username, password, 5432)

class valores:
    origen = 0
    destino = 0
    usuarioActual=""

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    if valores.usuarioActual != "":
        return render_template("dashboard.html")
    else:
        return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_found(e):
    return render_template("405.html")

@app.errorhandler(500)
def programer_error(e):
        return render_template("500.html", error=e)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    conn = psycopg2.connect(conn_string)
    conn2 = psycopg2.connect(conn_string)
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            cursor = conn.cursor()
            cursor2 = conn2.cursor()

            salida = ""
            salida2 = ""

            cursor.execute("SELECT nombre FROM usuario where nombre = (%s)", [request.form['username']])
            cursor2.execute("SELECT password FROM usuario where nombre = (%s)", [request.form['username']])

            for row in cursor:
                salida += str(row[0])
            for row in cursor2:
                salida2 += str(row[0])

            if attempted_username == salida and sha256_crypt.verify(attempted_password, salida2):
                valores.usuarioActual = salida
                return redirect((url_for('dashboard')))
            else:
                error = "Invalid Credentials. Please try again"
        return render_template("login.html", error = error)

    except Exception as e:
            return render_template("login.html", error = error)


@app.route('/register/', methods=['GET', 'POST'])
def registro():
    error = ''
    conn = psycopg2.connect(conn_string)
    salida = ''
    try:
        if request.method == "POST":
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            passwordEncrypt = sha256_crypt.encrypt(password)
            confirm = request.form['confirm']
            cursor = conn.cursor()
            if password == confirm:
                cursor.execute("INSERT into usuario (nombre, email, password) values (%s, %s, %s)",
                               [str(username), str(email), str(passwordEncrypt)])
                conn.commit()
                cursor.execute("SELECT nombre FROM usuario where nombre = (%s)", [request.form['username']])
                for row in cursor:
                    salida += str(row[0])
                valores.usuarioActual = salida
                return redirect((url_for('dashboard')))
            else:
                error = "Password does not match each other, please try again"
        return render_template("registro.html", error=error)

    except Exception as e:
        return render_template("registro.html", error=error)

@app.route('/jugar/', methods=['GET', 'POST'])
def jugar():
    if valores.usuarioActual != "":
        return render_template('pong.html')
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True, port=8000, host='0.0.0.0')

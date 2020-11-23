from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
   host="127.0.0.1",
   user="root",
   passwd="2408",
   database='mydb'
)
mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template("index.html")

@app.route('/add_contact', methods= ['POST'])
def add_contact():
    if request.method == 'POST':
        Rut_persona= request.form['RUT persona']
        Nombre_persona= request.form['Nombre persona']
        Direccion_vivienda= request.form['Direccion vivienda']
        cur = db.cursor()
        cur.execute('INSERT INTO `persona` (`RUT persona`, `Nombre persona`, `Direccion vivienda`) VALUES (%s,%s, %s);', (Rut_persona, Nombre_persona, Direccion_vivienda))
        db.commit()
        return 'received'

@app.route('/edit')
def edit_contact():
    return 'edit contact'

@app.route('/delete')
def delete_contact():
    return 'delete contact'


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
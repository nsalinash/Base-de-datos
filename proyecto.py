from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import mysql.connector

#conexion hacia Mysql
app = Flask(__name__)
db = mysql.connector.connect(
   host="127.0.0.1",
   user="root",
   passwd="pass",
   database='mydb'
)
mysql = MySQL(app)
#Configuracion para la pagina
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur= db.cursor()
    cur.execute('SELECT * FROM `persona`')
    data= cur.fetchall()
    return render_template("index.html", persona = data)

@app.route('/add_contact', methods= ['POST'])
def add_contact():
    if request.method == 'POST':
        Rut_persona= request.form['RUT persona']
        Nombre_persona= request.form['Nombre persona']
        Direccion_vivienda= request.form['Direccion vivienda']
        cur = db.cursor()
        cur.execute('INSERT INTO `persona` (`RUT persona`, `Nombre persona`, `Direccion vivienda`) VALUES (%s,%s, %s);', (Rut_persona, Nombre_persona, Direccion_vivienda))
        db.commit()
        flash('Se ha registrado correctamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = db.cursor()
    cur.execute("SELECT * FROM `persona` WHERE `RUT persona` = '{}' ".format(id))
    data= cur.fetchall()
    print(data[0])
    return 'recevied'
    
    #return render_template('edit-contact.html', contact = data[0])

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = db.cursor()
    cur.execute('DELETE FROM `persona` WHERE `RUT persona` = {0}'.format(id))
    db.commit()
    flash('Se ha eliminado correctamente compi')
    return redirect(url_for('Index'))



if __name__ == '__main__':
    app.run(port = 3000, debug = True)

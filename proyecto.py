from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import mysql.connector

#conexion hacia Mysql
app = Flask(__name__)
db = mysql.connector.connect(
   host="127.0.0.1",
   user="root",
   passwd="2408",
   database='mybdp'
)
mysql = MySQL(app)
#Configuracion para la pagina
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    return render_template("index.html")


@app.route('/agregar')
def agregar():
    cur= db.cursor()
    cur.execute('SELECT * FROM `persona`')
    data= cur.fetchall()

    return render_template("agregar.html", persona = data)    

@app.route('/genericos')
def genericos():
    cur = db.cursor()
    cur.execute('SELECT * FROM lista_de_precio_medicamento_generico')
    data = cur.fetchall()
    return render_template("genericos.html", generico = data)

@app.route('/receta')
def receta():
    cur = db.cursor()
    cur.execute("SELECT * from receta")
    data = cur.fetchall()
    return render_template("receta.html", receta = data)


@app.route('/add_contact', methods= ['POST'])
def add_contact():
    if request.method == 'POST':
        Rut_persona= request.form['RUT_persona']
        Nombre_persona= request.form['Nombre_persona']
        Direccion_vivienda= request.form['Direccion_vivienda']
        Comuna = request.form['Comuna']
        cur = db.cursor()
        #cur2 = db.cursor()
        cur.execute('INSERT INTO `persona` (`RUT_persona`, `Nombre_persona`, `Direccion_vivienda`, `MUNICIPIO_Nombre_municipio`) VALUES (%s,%s, %s, %s);', (Rut_persona, Nombre_persona, Direccion_vivienda, Comuna))
        #cur2.execute('INSERT INTO `inscrito` (`PERSONA_RUT_persona`, `MUNICIPIO_Nombre_municipio`) VALUES (%s, %s);', (Rut_persona, Comuna))

        db.commit()
        flash('Se ha registrado correctamente')
        return redirect(url_for('agregar'))



@app.route('/edit/<id>')
def get_contact(id):
    cur = db.cursor()
    cur.execute("SELECT * FROM `persona` WHERE `RUT_persona` = '{}' ".format(id))
    data= cur.fetchall()
    return render_template('edit-contact.html', persona = data)
    


@app.route('/add_medicamentos', methods= ['POST'])
def add_medicamentos():
    if request.method == 'POST':
        Nombre_medicamento= request.form['Nombre_medicamento']
        ID_medicamento= request.form['ID_medicamento']
        Tipo_farmaco= request.form['Tipo_farmaco']
        cur = db.cursor()
        cur.execute('INSERT INTO medicamento (Nombre_medicamento, ID_medicamento, Tipo_farmaco) VALUES (%s,%s, %s);', (Nombre_medicamento, ID_medicamento,Tipo_farmaco))
        db.commit()
        flash('Se ha registrado correctamente')
        return redirect(url_for('medicamentos'))


@app.route('/medicamentos')
def medicamentos():
    cur= db.cursor()
    cur.execute('SELECT * FROM medicamento')
    data= cur.fetchall()
    return render_template("medicamentos.html", medicamento = data)
    
            
@app.route('/venta')
def venta():
    cur = db.cursor()
    cur.execute("SELECT * FROM medicamento")
    data = cur.fetchall()

    return render_template("venta.html", venta = data)


@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        RUT_persona = request.form['RUT_persona']
        Nombre_persona = request.form['Nombre_persona']
        Direccion_vivienda = request.form['Direccion_vivienda']
        cur = db.cursor()
        cur.execute("UPDATE persona SET `RUT_persona` = '{}', `Nombre_persona` = '{}', `Direccion_vivienda`= '{}' WHERE `RUT_persona` = '{}';".format(RUT_persona, Nombre_persona, Direccion_vivienda, id))
        db.commit()
        flash('Contacto actualizado satisfactoriamente')
        return redirect(url_for('agregar'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = db.cursor()
    cur.execute('DELETE FROM `persona` WHERE `RUT_persona` = {}'.format(id))
    db.commit()
    flash('Se ha eliminado correctamente')
    return redirect(url_for('agregar'))

@app.route('/mostrar/<id>')
def mostrar_farmacias(id):
    cur = db.cursor()

    print("Id completa = ",id)
    cur.execute("SELECT pertenece.MUNICIPIO_Nombre_municipio, farmacia.Direccion, farmacia.Nombre_farmacia FROM pertenece INNER JOIN farmacia ON pertenece.MUNICIPIO_Nombre_municipio = '{}' and pertenece.FARMACIA_Direccion = farmacia.Direccion".format(id))
    data = cur.fetchall()
    print("data = ",data)
    return render_template('farmacia_cercana.html', farmacia = data)

@app.route('/farmacias')
def farmacias():
    cur = db.cursor()
    cur.execute('SELECT * FROM `farmacia`')
    data = cur.fetchall()
    return render_template("farmacias.html", farmacia = data)

@app.route('/buscar')
def buscar():
    return render_template("buscar.html")

@app.route('/addfarmacia', methods = ['POST'])
def add_farmacia():
    if request.method == 'POST':
        Direccion = request.form['Direccion']
        Nombre = request.form['Nombre_farmacia']
        Comuna = request.form['Comuna']
        cur = db.cursor()
        cur2 = db.cursor()
        cur.execute('INSERT INTO `farmacia` (`Direccion`, `Nombre_farmacia`, `MUNICIPIO_Nombre_municipio`) VALUES (%s,%s,%s);', (Direccion, Nombre, Comuna))
        cur2.execute('INSERT INTO `pertenece` (`MUNICIPIO_Nombre_municipio`, `FARMACIA_Direccion`) VALUES (%s, %s);', (Comuna, Direccion ))
        db.commit()
        flash('Se ha registrado correctamente')
        return redirect(url_for('farmacias'))
        #return render_template("farmacias.html")

@app.route('/buscarfarmacia', methods = ['POST'])
def buscar_farmacia():
    if request.method == 'POST':
        Comuna = request.form['Comuna']
        cur = db.cursor()
        #cur.execute("SELECT pertenece.MUNICIPIO_Nombre_municipio, farmacia.Direccion, farmacia.Nombre_farmacia FROM pertenece INNER JOIN farmacia ON pertenece.MUNICIPIO_Nombre_municipio = '{}' and pertenece.FARMACIA_Direccion = farmacia.Direccion".format(Comuna))
        cur.execute("SELECT * FROM farmacia WHERE MUNICIPIO_Nombre_municipio = '{}' ".format(Comuna))
        data = cur.fetchall()
        print(data)
        return render_template("buscar.html", pertenece = data)



if __name__ == '__main__':
    app.run(port = 3000, debug = True) 
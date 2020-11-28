@app.route('/receta')
def receta():
    cur = db.cursor()
    cur.execute("SELECT * from receta")
    data = cur.fetchall()
    return render_template("receta.html", receta = data)

@app.route('/editarr/<id>', methods = ['POST'])
def add_recipe():
    if request.method == 'POST':
        Fecha_prescripcion = request.form['FECHA_DE_PRESCRIPCIÓN_DDMMAA']
        Medicamento = request.form['MEDICAMENTO_Nombre_medicamento']
        Rut_persona = request.form['PERSONA_RUT_persona']
        Rut_medico = request.form['MEDICO_RUT_Medico']
        cur = db.cursor()
        cur.execute('INSERT INTO receta (FECHA_DE_PRESCRIPCIÓN_DDMMAA, MEDICAMENTO_Nombre_medicamento, PERSONA_RUT_persona, MEDICO_RUT_Medico) VALUES (%s, %s, %s, %s);', (Fecha_prescripcion, Medicamento, Rut_persona, Rut_medico))
        db.commit()
        flash('Se ha registrado correctamente')
        return redirect(url_for('receta'))

@app.route('/borrarr/<string:id>')
def delete_recipe(id):
    cur = db.cursor()
    cur.execute("DELETE FROM `receta` WHERE `PERSONA_RUT_persona` = '{}'".format(id))
    db.commit()
    flash('Se ha eliminado correctamente')
    return redirect(url_for('receta'))

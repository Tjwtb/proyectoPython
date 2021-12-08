from flask import Flask
#Xml
import xml.etree.ElementTree as xml
#solicitudes de informacion //urlfor y flash nuevo
from flask import render_template, request, redirect, url_for, flash
#acceso a la bd
from flaskext.mysql import MySQL
#nuevo
from flask import send_from_directory
from datetime import datetime
#nuevo
import os
#modulos personales
from modulos import *

app= Flask(__name__)
app.secret_key="Johanadmin"

mysql = MySQL()
#conexion a la bd
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tecalumnos'
#crear la conexion con los datos
mysql.init_app(app)

#nuevo
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

#nuevo
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

#La app ira a la raiz
@app.route('/')
def index():
    conn= mysql.connect()
    #en cursor guardamos lo que vamos a ejecutar
    cursor=conn.cursor()
    cursor.execute(Select())
    estudiantes=cursor.fetchall()
    print(estudiantes)
    #cerrar la ejecucion
    conn.commit()
    return render_template('estudiantes/index.html', estudiantes=estudiantes)

#mantener como prueba
@app.route('/destroy/<int:id>')
def destroy(id):
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("Select foto FROM estudiantes WHERE id=%s",(id))
    #nuevo
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
    cursor.execute(Delete(),(id))
    #terminanuevo
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM estudiantes WHERE id=%s",(id))
    estudiantes=cursor.fetchall()
    conn.commit()
    return render_template('estudiantes/edit.html', estudiantes=estudiantes)

@app.route('/datos/<int:id>')
def datos(id):

    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM estudiantes WHERE id=%s",(id))
    estudiantes=cursor.fetchall()
    conn.commit()
    return render_template('estudiantes/datos.xml', estudiantes=estudiantes)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _ncontrol=request.form['txtNControl']
    _carrera=request.form['txtCarrera']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    if _nombre == '' or _apellido=='' or _correo=='' or _ncontrol=='' or _carrera=='' or _foto=='':
        flash('Si vas a editar el registro no puedes dejar espacios vacios')
        return redirect(url_for('edit',id = id))
    
    #aqui va
    sql="UPDATE estudiantes SET nombre=%s, apellido=%s, correo=%s, ncontrol=%s, carrera=%s WHERE id=%s;"
    datos=(_nombre,_apellido,_correo,_ncontrol,_carrera, id)
    conn= mysql.connect()
    cursor=conn.cursor()

    #nuevo
    now = datetime.now()
    tiempo=now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto= tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)    
        cursor.execute("SELECT foto FROM estudiantes WHERE id=%s", id)
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE estudiantes SET foto=%s where id=%s",(nuevoNombreFoto,id))
        conn.commit()
    #terminanuevo
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/create')
def create():
    return render_template('estudiantes/create.html')

@app.route('/info')
def info():
    return render_template('estudiantes/info.html')


@app.route('/store', methods=['POST'])
def storage():

    _nombre=request.form['txtNombre']
    _apellido=request.form['txtApellido']
    _correo=request.form['txtCorreo']
    _ncontrol=request.form['txtNControl']
    _carrera=request.form['txtCarrera']
    _foto=request.files['txtFoto']


    if _nombre == '' or _apellido=='' or _correo=='' or _ncontrol=='' or _carrera=='' or _foto=='':
        flash('Recuerda llenar todos los campos solicitados')
        return redirect(url_for('create'))


    ahora= datetime.now()
    tiempo=ahora.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
     
    #aqui va
    datos=(_nombre,_apellido,_correo,_ncontrol,_carrera, nuevoNombreFoto)
    conn= mysql.connect()
    cursor=conn.cursor()
    cursor.execute(Insert(),datos)
    conn.commit()
    return redirect('/')
    #return render_template('estudiantes/index.html')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import sqlite3 

app = Flask(__name__)
app.secret_key = 'cultura'

#Respaldo por si me mando alguna cagada tratando de hacer el crud con las respuestas incluidas
#---------------------CRUD-----------------------
#--------------CONSULTAR PREGUNTAS-------   
@app.route('/consultarPreguntas')
def consultarPreguntas():
    return render_template('consultar.html')

@app.route('/editarRespuesta', methods=['GET','PUT'])
def modificarRespuesta():
  if request.method == "PUT":
    respuesta = request.form["respuesta"]
    respuestaModificada = request.form["respuestaModificada"]
    categoriaModificada= request.form["categoriaModificada"]
    esCorrectaModificada = request.form["esCorrectaModificada"]
    idPreguntaModificado = request.form["idPreguntaModificado"]
    conn = sqlite3.connect('base_de_datos.db')
    agregarDato = f'''UPDATE Respuestas SET contenido_respuesta="{respuestaModificada}", categoria = "{categoriaModificada}", id_pregunta = "{idPreguntaModificado}", es_correcta = "{esCorrectaModificada}"  WHERE contenido_respuesta="{respuesta}"'''
    tomarId = (f'''SELECT DISTINCT Preguntas.id_pregunta FROM Preguntas INNER JOIN Respuestas ON Preguntas.id_pregunta = Respuestas.id_pregunta WHERE contenido_p = "{respuesta}";''')
    conn.execute(agregarDato, tomarId)
    conn.commit()
    return jsonify(f"La pregunta {respuesta} cambio a: {respuestaModificada}")
@app.route('/extraer')
def extraerPreguntas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT contenido_pregunta, Preguntas.categoria, Preguntas.id_pregunta, id_respuesta, contenido_respuesta, es_correcta FROM Preguntas INNER JOIN Respuestas ON Respuestas.id_pregunta = Preguntas.id_pregunta")
  resu = conn.execute(consulta).fetchall()
  print(resu)
  return jsonify(resu)

#---------------------AGREGAR---------------  
@app.route('/agregarPreguntas')
def agregarPreguntas():
    return render_template('agregar.html')

@app.route('/agregar', methods=['GET','POST'])
def crearPreguntas():
  if request.method == "POST":
    preguntaAAgregar = request.form["preguntaAAgregar"]
    categoriaAAgregar = request.form["categoriaAAgregar"]
    conn = sqlite3.connect('base_de_datos.db')
    agregarDato = ("INSERT INTO Respuestas (contenido_pregunta, es_correcta, id_pregunta, categoria) VALUES ('Respuesta diferente', 0, 2, 'Musica') SELECT DISTINCT Preguntas.id_pregunta, Preguntas.categoria FROM Preguntas INNER JOIN Respuestas ON Preguntas.id_pregunta = Respuestas.id_pregunta WHERE contenido_pregunta ='¿Cual fue la primera canción de Duki?'")
    
    conn.execute(agregarDato)
    conn.commit()
    conn.close()
    return jsonify(True)
  else:
    return jsonify(False)

#-------------------EDITAR-----------------
@app.route('/listaPreguntasEditar')
def editarPreguntas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT contenido_pregunta FROM Preguntas")
  preguntas = conn.execute(consulta).fetchall()
  print(preguntas)
  return render_template("editar.html", preguntas = preguntas)

@app.route('/editar', methods=['GET','PUT'])
def modificarPregunta():
  if request.method == "PUT":
    pregunta = request.form["pregunta"]
    preguntaModificada = request.form["preguntaModificada"]
    conn = sqlite3.connect('base_de_datos.db')
    agregarDato = f'''UPDATE Preguntas SET contenido_pregunta="{preguntaModificada}" WHERE contenido_pregunta="{pregunta}"'''
    conn.execute(agregarDato)
    conn.commit()
    return jsonify(f"La pregunta {pregunta} cambio a: {preguntaModificada}")

#-------------------ELIMINAR--------------
@app.route('/listaPreguntasEliminar')
def eliminarPreguntas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT contenido_pregunta FROM Preguntas")
  preguntas = conn.execute(consulta).fetchall()
  print(preguntas)
  return render_template("borrar.html", preguntas = preguntas)
  
@app.route('/eliminarPreg', methods=['GET','DELETE'])
def eliminar():
  if request.method=="DELETE":
    preguntaAEliminar = request.form["preguntaAEliminar"]
    print(preguntaAEliminar)
    conn = sqlite3.connect('base_de_datos.db')
    eliminarDato = (f'''DELETE FROM Preguntas WHERE contenido_pregunta="{preguntaAEliminar}"''')
    conn.execute(eliminarDato).fetchall()
    conn.commit()
    conn.close()
    return jsonify(f"Se elimino la pregunta: {preguntaAEliminar}") 
  
#--------------------USUARIOS-------------
@app.route('/consultarUsuarios')
def consultarUsuarios():
    return render_template('consultarUsuario.html')
  
@app.route('/extraerUsuarios')
def extraerUsuarios():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT * FROM Jugadores WHERE nombre_jugador NOT LIKE 'admin'")
  resu=conn.execute(consulta).fetchall()
  print(resu)
  return jsonify(resu)

@app.route('/mostrarUsuariosAEliminar')
def eliminarUsuarios():
    conn=sqlite3.connect('base_de_datos.db')
    consulta=("SELECT nombre_jugador FROM Jugadores WHERE nombre_jugador NOT LIKE 'admin'")
    usuarios=conn.execute(consulta).fetchall()
    print(usuarios)
    conn.commit()
    conn.close()
    return render_template('borrarUsuario.html', usuarios=usuarios)
  
@app.route('/eliminarUsuario', methods=['GET','DELETE'])
def eliminarUsuario():
  if request.method == "DELETE":
    usuarioAEliminar = request.form["usuarioAEliminar"]
    conn = sqlite3.connect('base_de_datos.db')
    eliminarDato = (f'''DELETE FROM Jugadores WHERE nombre_jugador="{usuarioAEliminar}"''')
    conn.execute(eliminarDato)
    conn.commit()
    conn.close()
    return jsonify(f"Se elimino el usuario: {usuarioAEliminar}")

@app.route('/agregarRespuesta', methods=['GET','POST'])
def crearRespuesta():
  if request.method == "POST":
    pregunta = request.form["preguntaLista"]
    respuestaAAgregar = request.form["respuestaAAgregar"]
    esCorrecta = request.form["esCorrecta"]
    conn = sqlite3.connect('base_de_datos.db')
    tomarId= (f'''INSERT INTO Respuestas(contenido_respuesta, es_correcta)
VALUES ("{respuestaAAgregar}", "{esCorrecta}";''')
    conn.execute(tomarId)
    agregarDato = (f''' INSERT INTO Respuestas (contenido_respuesta, es_correcta) VALUES ("{respuestaAAgregar}","{esCorrecta}") WHERE contenido_pregunta = {pregunta} SELECT contenido_pregunta FROM Preguntas INNER JOIN Respuestas ON Respuestas.id_pregunta = Preguntas.id_pregunta''')
    conn.execute(agregarDato)
    conn.commit()
    conn.close()
    return jsonify(True)
  else:
    return jsonify(False)

'''
@app.route('/nose')
def nose():
    ranking=[]
    conn = sqlite3.connect('base_de_datos.db')
    curr = conn.execute("SELECT * FROM Jugadores ORDER BY ranking DESC LIMIT 3").fetchall()
    conn.commit()
    print(curr)
    for x in curr:
      dicc = {}
      dicc['id_jugador'] = x[0]
      dicc['nombre'] = x[1]
      dicc['contraseña'] = x[2]
      dicc['ranking'] = x[3]
    ranking.append(dicc)
    return render_template(ranking = ranking)
'''
app.run(host='0.0.0.0', port=81)





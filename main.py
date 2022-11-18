from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import sqlite3 

app = Flask(__name__)
app.secret_key = 'cultura'

#--------------------INICIO---------------------  
@app.route('/')
def index():
    return render_template('index.html')
#---------------------LOGIN-------------------------
@app.route('/login', methods=['POST','GET'])
def login():
  return render_template('login.html')
  
@app.route('/ingresar', methods=['POST','GET'])
def ingresar():
  msg=''
  if request.method=='POST':
    nombre=request.form['nombre']
    session['nombre']=nombre
    contraseña=request.form['contraseña']
    session['contraseña']=contraseña
    con= sqlite3.connect('base_de_datos.db')
    cur=con.cursor()
    curr = con.cursor()
    cur.execute(f'''SELECT * FROM Jugadores WHERE nombre_jugador="{nombre}"''')
    curr.execute(f'''SELECT * FROM Jugadores WHERE contraseña="{contraseña}"''')
    resultado=cur.fetchall()
    resultado2 = curr.fetchall()
    con.commit()
    if len(resultado)==0:
      msg="No existe el usuario, registrate" 
      return render_template('registro.html', msg=msg)
    if len(resultado2)==0:
      msg="Contraseña incorrecta"
      return render_template('login.html', msg=msg)
    else:
      cur.execute(f'''SELECT nombre_jugador, contraseña From Jugadores WHERE nombre_jugador= "{nombre}" AND contraseña="{contraseña}"''')
      return render_template('cuentaIniciada.html', nombre=nombre)
#-------------------REGISTRO------------------------
@app.route('/registro', methods=['POST','GET'])
def registro():
  return render_template('registro.html')

@app.route('/registrarse', methods=['POST','GET'])
def registrarse2():
  msg=''
  if request.method=='POST':
    nombre=request.form['nombre']
    session['nombre']=nombre
    contraseña=request.form['contraseña']
    session['contraseña']=contraseña
    con= sqlite3.connect('base_de_datos.db')
    cur=con.cursor()
    cur.execute(f'''SELECT * FROM Jugadores WHERE nombre_jugador="{nombre}"''')
    data=cur.fetchall()
    if data:
      msg="Ya existe la cuenta, logueate"
      return render_template('login.html', msg=msg)
    else:
      cur.execute(f"""INSERT INTO Jugadores (nombre_jugador, contraseña) VALUES('{nombre}','{contraseña}');""")
      con.commit()
      con.close()
  return render_template('cuentaCreada.html')

#---------------------REDIRECCION----------------
@app.route("/cuentaCreada")
def cuentaCreada():
  nombre=request.form['nombre']
  session['nombre']=nombre
  return render_template('cuentaCreada.html', nombre=nombre)
  
#------------------------LOG OUT--------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#--------------------CATEGORIAS-----------------------
@app.route("/categorias")
def categorias():
  return render_template('categorias_registro.html')
#---------------------INICIO----------------------
@app.route("/inicio")
def inicio():
  return render_template('categorias.html')
#------------------USUARIO ADMIN-----------------
@app.route('/admin')
def admin():
  return render_template('usuarioAdmin.html')
#---------------------CRUD-----------------------
#--------------CONSULTAR PREGUNTAS-------   
@app.route('/consultarPreguntas')
def consultarPreguntas():
    return render_template('consultar.html')
  
@app.route('/extraerPreguntas')
def extraerPreguntas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT * FROM Preguntas")
  resu = conn.execute(consulta).fetchall()
  return jsonify(resu)

@app.route('/extraerRespuestas')
def extraerRespuestas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT contenido_pregunta, Preguntas.categoria, Preguntas.id_pregunta, id_respuesta, contenido_respuesta, es_correcta FROM Preguntas INNER JOIN Respuestas ON Respuestas.id_pregunta = Preguntas.id_pregunta ORDER BY Respuestas.id_pregunta ASC")
  resu = conn.execute(consulta).fetchall()
  return jsonify(resu)
#---------------------AGREGAR---------------  
@app.route('/agregarPreguntas')
def agregarPreguntas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT contenido_pregunta FROM Preguntas")
  preguntas = conn.execute(consulta).fetchall()
  return render_template("agregar.html", preguntas = preguntas)

@app.route('/agregarPregunta', methods=['GET','POST'])
def crearPreguntas():
  if request.method == "POST":
    preguntaAAgregar = request.form["preguntaAAgregar"]
    categoriaAAgregar = request.form["categoriaAAgregar"]
    conn = sqlite3.connect('base_de_datos.db')
    agregarDato = (f'''INSERT INTO Preguntas (contenido_pregunta, categoria) VALUES ("{preguntaAAgregar}","{categoriaAAgregar}")''')
    conn.execute(agregarDato)
    conn.commit()
    conn.close()
    return jsonify(True)
  else:
    return jsonify(False)

#https://stackoverflow.com/questions/29522298/sqlite-insert-into-select-how-to-insert-data-of-join-of-3-existing-tables-i
@app.route('/agregarRespuesta', methods=['GET','POST'])
def crearRespuesta():
  if request.method == "POST":
    pregunta=request.form["preguntaLista"]
    respuesta = request.form["respuesta"]
    categoria = request.form["categoria"]
    esCorrecta = request.form["esCorrecta"]
    idPregunta = request.form["idPregunta"]
    conn = sqlite3.connect('base_de_datos.db')
    tomarId= (f'''SELECT DISTINCT Preguntas.id_pregunta FROM Preguntas WHERE contenido_pregunta = "{pregunta}"''')
    resu = conn.execute(tomarId).fetchall()
    agregarDato = (f'''INSERT INTO Respuestas(contenido_respuesta, categoria, id_pregunta, es_correcta)
VALUES ("{respuesta}", "{categoria}", "{esCorrecta}","{idPregunta}")''')
    resu2=conn.execute(agregarDato)
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
  consulta2= ("SELECT contenido_respuesta FROM Respuestas ORDER BY id_pregunta ASC")
  respuestas = conn.execute(consulta2).fetchall()
  consulta3= ("SELECT DISTINCT id_pregunta FROM Respuestas")
  id = conn.execute(consulta3).fetchall()
  return render_template("editar.html", preguntas = preguntas, respuestas=respuestas, id=id)

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

@app.route('/editarRespuesta', methods=['GET','PUT'])
def modificarRespuesta():
  if request.method == "PUT":
    respuesta = request.form["respuesta"]
    respuestaModificada = request.form["respuestaModificada"]
    conn = sqlite3.connect('base_de_datos.db')
    agregarDato = (f'''UPDATE Respuestas SET contenido_respuesta="{respuestaModificada}" WHERE contenido_respuesta="{respuesta}"''')
    conn.execute(agregarDato)
    conn.commit()
    return jsonify(f"La respuesta {respuesta} cambio a: {respuestaModificada}")
#-------------------ELIMINAR--------------
@app.route('/listaPreguntasEliminar')
def eliminarPreguntas():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT contenido_pregunta FROM Preguntas")
  preguntas = conn.execute(consulta).fetchall()
  consulta2=("SELECT contenido_respuesta FROM Respuestas ORDER BY id_pregunta ASC")
  respuestas=conn.execute(consulta2).fetchall()
  return render_template("borrar.html", preguntas=preguntas, respuestas=respuestas)
  
@app.route('/eliminarPreg', methods=['GET','DELETE'])
def eliminarPreg():
  if request.method=="DELETE":
    preguntaAEliminar = request.form["preguntaAEliminar"]
    conn = sqlite3.connect('base_de_datos.db')
    eliminarDato = (f'''DELETE FROM Preguntas WHERE contenido_pregunta="{preguntaAEliminar}"''')
    conn.execute(eliminarDato).fetchall()
    conn.commit()
    conn.close()
    return jsonify(f"Se elimino la pregunta: {preguntaAEliminar}") 

@app.route('/eliminarRta', methods=['GET','DELETE'])
def eliminarRta():
  if request.method=="DELETE":
    respuestaAEliminar = request.form["respuestaAEliminar"]
    conn = sqlite3.connect('base_de_datos.db')
    eliminarDato = (f'''DELETE FROM Respuestas WHERE contenido_respuesta="{respuestaAEliminar}"''')
    conn.execute(eliminarDato).fetchall()
    conn.commit()
    conn.close()
    return jsonify(f"Se elimino la respuesta: {respuestaAEliminar}") 

#--------------------USUARIOS-------------
@app.route('/consultarUsuarios')
def consultarUsuarios():
    return render_template('consultarUsuario.html')
  
@app.route('/extraerUsuarios')
def extraerUsuarios():
  conn = sqlite3.connect('base_de_datos.db')
  consulta = ("SELECT * FROM Jugadores WHERE nombre_jugador NOT LIKE 'admin'")
  resu=conn.execute(consulta).fetchall()
  return jsonify(resu)

@app.route('/mostrarUsuariosAEliminar')
def eliminarUsuarios():
    conn=sqlite3.connect('base_de_datos.db')
    consulta=("SELECT nombre_jugador FROM Jugadores WHERE nombre_jugador NOT LIKE 'admin'")
    usuarios=conn.execute(consulta).fetchall()
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

#https://stackoverflow.com/questions/19025127/storing-values-in-sqlite-database
#-------------PREGUNTAS LIBROS------------
@app.route('/preguntasLibros')
def preguntasLibros():
  afirmaciones=[]
  conn = sqlite3.connect('base_de_datos.db')

  cur = conn.execute("SELECT * FROM Preguntas WHERE categoria = 'Libros' ORDER BY random () LIMIT 12")
  for x in cur:
    dicc = {}
    dicc['id_pregunta'] = x[0]
    dicc['contenido'] = x[1]
    dicc['categoria'] = x[2]

    afirmaciones.append(dicc)
    
  conn.close()
  #----------------RESPUESTAS MUSICA------------
  respuestas = []
  conn = sqlite3.connect('base_de_datos.db')
  for pregunta in afirmaciones:
    cur = conn.execute(f"""SELECT * From Respuestas WHERE categoria = 'Libros' AND id_pregunta = {pregunta['id_pregunta']}""").fetchall()
    respuestasPregunta = []
    for y in cur:
      diccRta = {}
      diccRta['id_rta'] = y[0]
      diccRta['contenido_rta'] = y[1]
      diccRta['categoria_rta'] = y[2]
      diccRta['id_preg'] = y[3]
      diccRta['es_correcta'] = y[4]
      respuestasPregunta.append(diccRta) 
    respuestas.append(respuestasPregunta)  
  return render_template('preguntas.html', afirmaciones=afirmaciones, respuestas=respuestas)

#-------------PREGUNTAS MUSICA------------
@app.route('/preguntasMusica')
def preguntasMusica():
  afirmaciones=[]
  conn = sqlite3.connect('base_de_datos.db')

  cur = conn.execute("SELECT * FROM Preguntas WHERE categoria = 'Musica' ORDER BY random () LIMIT 12")
  for x in cur:
    dicc = {}
    dicc['id_pregunta'] = x[0]
    dicc['contenido'] = x[1]
    dicc['categoria'] = x[2]

    afirmaciones.append(dicc)
    
  conn.close()
  #----------------RESPUESTAS MUSICA------------
  respuestas = []
  conn = sqlite3.connect('base_de_datos.db')
  for pregunta in afirmaciones:
    cur = conn.execute(f"""SELECT * From Respuestas WHERE categoria = 'Musica' AND id_pregunta = {pregunta['id_pregunta']}""").fetchall()
    respuestasPregunta = []
    for y in cur:
      diccRta = {}
      diccRta['id_rta'] = y[0]
      diccRta['contenido_rta'] = y[1]
      diccRta['categoria_rta'] = y[2]
      diccRta['id_preg'] = y[3]
      diccRta['es_correcta'] = y[4]
      respuestasPregunta.append(diccRta) 
    respuestas.append(respuestasPregunta)  
  return render_template('preguntas.html', afirmaciones=afirmaciones, respuestas=respuestas)

 #-------------------------PREGUNTAS CINE------------------------
@app.route('/preguntasCine')
def preguntasCine():
  afirmaciones=[]
  conn = sqlite3.connect('base_de_datos.db')
  cur = conn.execute("SELECT * FROM Preguntas WHERE categoria = 'Cine' ORDER BY random() LIMIT 12")
  for x in cur:
    dicc = {}
    dicc['id_pregunta'] = x[0]
    dicc['contenido'] = x[1]
    dicc['categoria'] = x[2]

    afirmaciones.append(dicc)
    
  conn.close()
  #----------------RESPUESTAS CINE----------------
  respuestas = []
  conn = sqlite3.connect('base_de_datos.db')
  for pregunta in afirmaciones:
    cur = conn.execute(f"""SELECT * From Respuestas WHERE categoria = 'Cine' AND id_pregunta = {pregunta['id_pregunta']}""").fetchall()
    respuestasPregunta = []
    for y in cur:
      diccRta = {}
      diccRta['id_rta'] = y[0]
      diccRta['contenido_rta'] = y[1]
      diccRta['categoria_rta'] = y[2]
      diccRta['id_preg'] = y[3]
      diccRta['es_correcta'] = y[4]
      respuestasPregunta.append(diccRta) 
    respuestas.append(respuestasPregunta)  
  return render_template('preguntas.html', afirmaciones=afirmaciones, respuestas=respuestas)

#-------------------------PREGUNTAS MIX------------------------
@app.route('/preguntasMix')
def preguntasMix():
  afirmaciones=[]
  conn = sqlite3.connect('base_de_datos.db')
  cur = conn.execute("SELECT * FROM Preguntas ORDER BY random() LIMIT 12")
  for x in cur:
    dicc = {}
    dicc['id_pregunta'] = x[0]
    dicc['contenido'] = x[1]
    dicc['categoria'] = x[2]

    afirmaciones.append(dicc)
    
  conn.close()
  #----------------RESPUESTAS MIX-----------
  respuestas = []
  conn = sqlite3.connect('base_de_datos.db')
  for pregunta in afirmaciones:
    cur = conn.execute(f"""SELECT * From Respuestas WHERE id_pregunta = {pregunta['id_pregunta']}""").fetchall()
    respuestasPregunta = []
    for y in cur:
      diccRta = {}
      diccRta['id_rta'] = y[0]
      diccRta['contenido_rta'] = y[1]
      diccRta['categoria_rta'] = y[2]
      diccRta['id_preg'] = y[3]
      diccRta['es_correcta'] = y[4]
      respuestasPregunta.append(diccRta) 
    respuestas.append(respuestasPregunta)  
  return render_template('preguntas.html', afirmaciones=afirmaciones, respuestas=respuestas)
#--------------------FIN DEL JUEGO MUSICA---------------
@app.route('/finJuegoMusica/<puntaje>/<tiempo>', methods = ["POST", "GET"])
def finJuegoMusica(puntaje, tiempo):
  nombre=session['nombre']
  ranking=[]
  con = sqlite3.connect('base_de_datos.db')
  cur=con.cursor() 
  tomarRanking = cur.execute(f'''SELECT ranking_musica FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  puntos = tomarRanking.fetchone()
  tomarTiempo = cur.execute(f'''SELECT tiempo_musica FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  tiempos = tomarTiempo.fetchone()
  con.commit()
  if int(puntaje) > puntos[0] or int(puntaje) >= puntos[0] and float(tiempo) < tiempos[0]:
    actualizarRanking = cur.execute(f"""UPDATE Jugadores SET ranking_musica='{puntaje}', tiempo_musica='{tiempo}' WHERE nombre_jugador = '{nombre}'""").fetchall()
    con.commit()
  mostrarRanking = cur.execute("SELECT * FROM Jugadores ORDER BY ranking_musica DESC LIMIT 3")
  for x in mostrarRanking:
    dicc = {}
    dicc['id'] = x[0]
    dicc['nombre'] = x[1]
    dicc['contraseña'] = x[2]
    dicc['ranking_musica'] = x[3]
    dicc['tiempo_musica'] = x[7] 
    ranking.append(dicc)
  con.commit() 
  con.close()
  return render_template('finDelJuegoMusica.html', nombre=nombre, puntaje=puntaje, ranking=ranking, tiempoFinal=tiempo) 

#--------------------FIN DEL JUEGO LIBROS---------------
@app.route('/finJuegoLibros/<puntaje>/<tiempo>', methods = ["POST", "GET"])
def finJuegoLibros(puntaje, tiempo):
  nombre=session['nombre']
  rankingLibros=[]
  con = sqlite3.connect('base_de_datos.db')
  cur=con.cursor() 
  tomarRanking = cur.execute(f'''SELECT ranking_libros FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  puntos = tomarRanking.fetchone()
  tomarTiempo = cur.execute(f'''SELECT tiempo_libros FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  tiempos = tomarTiempo.fetchone()
  con.commit()
  if int(puntaje) > puntos[0] or int(puntaje) >= puntos[0] and float(tiempo) < tiempos[0]:
    actualizarRanking = cur.execute(f"""UPDATE Jugadores SET ranking_libros='{puntaje}', tiempo_libros='{tiempo}' WHERE nombre_jugador = '{nombre}'""").fetchall()
    con.commit()
  mostrarRanking = cur.execute("SELECT * FROM Jugadores ORDER BY ranking_libros DESC LIMIT 3")
  for x in mostrarRanking:
    dicc = {}
    dicc['id'] = x[0]
    dicc['nombre'] = x[1]
    dicc['contraseña'] = x[2]
    dicc['ranking_libros'] = x[4]
    dicc['tiempo_libros'] = x[8] 
    rankingLibros.append(dicc)
  con.commit() 
  con.close()
  return render_template('finDelJuegoLibros.html', nombre=nombre, puntaje=puntaje, rankingLibros=rankingLibros, tiempoFinal=tiempo) 


#--------------------FIN DEL JUEGO CINE---------------
@app.route('/finJuegoCine/<puntaje>/<tiempo>', methods = ["POST", "GET"])
def finJuegoCine(puntaje, tiempo):
  nombre=session['nombre']
  rankingCine=[]
  con = sqlite3.connect('base_de_datos.db')
  cur=con.cursor() 
  tomarRanking = cur.execute(f'''SELECT ranking_cine FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  puntos = tomarRanking.fetchone()
  tomarTiempo = cur.execute(f'''SELECT tiempo_cine FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  tiempos = tomarTiempo.fetchone()
  con.commit()
  if int(puntaje) > puntos[0] or int(puntaje) >= puntos[0] and float(tiempo) < tiempos[0]:
    actualizarRanking = cur.execute(f"""UPDATE Jugadores SET ranking_cine='{puntaje}', tiempo_cine='{tiempo}' WHERE nombre_jugador = '{nombre}'""").fetchall()
    con.commit()
  mostrarRanking = cur.execute("SELECT * FROM Jugadores ORDER BY ranking_cine DESC LIMIT 3")
  for x in mostrarRanking:
    dicc = {}
    dicc['id'] = x[0]
    dicc['nombre'] = x[1]
    dicc['contraseña'] = x[2]
    dicc['ranking_cine'] = x[5]
    dicc['tiempo_cine'] = x[9] 
    rankingCine.append(dicc)
  con.commit() 
  con.close()
  return render_template('finDelJuegoCine.html', nombre=nombre, puntaje=puntaje, rankingCine=rankingCine, tiempoFinal=tiempo) 

#--------------------FIN DEL JUEGO MIX---------------
@app.route('/finJuegoMix/<puntaje>/<tiempo>', methods = ["POST", "GET"])
def finJuegoMix(puntaje, tiempo):
  nombre=session['nombre']
  rankingMix=[]
  con = sqlite3.connect('base_de_datos.db')
  cur=con.cursor() 
  tomarRanking = cur.execute(f'''SELECT ranking_mix FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  puntos = tomarRanking.fetchone()
  tomarTiempo = cur.execute(f'''SELECT tiempo_mix FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  tiempos = tomarTiempo.fetchone()
  con.commit()
  if int(puntaje) > puntos[0] or int(puntaje) >= puntos[0] and float(tiempo) < tiempos[0]:
    actualizarRanking = cur.execute(f"""UPDATE Jugadores SET ranking_mix='{puntaje}', tiempo_mix='{tiempo}' WHERE nombre_jugador = '{nombre}'""").fetchall()
    con.commit()
  mostrarRanking = cur.execute("SELECT * FROM Jugadores ORDER BY ranking_mix DESC LIMIT 3")
  for x in mostrarRanking:
    dicc = {}
    dicc['id'] = x[0]
    dicc['nombre'] = x[1]
    dicc['contraseña'] = x[2]
    dicc['ranking_mix'] = x[6]
    dicc['tiempo_mix'] = x[10] 
    rankingMix.append(dicc)
  con.commit() 
  con.close()
  return render_template('finDelJuegoMix.html', nombre=nombre, puntaje=puntaje, rankingMix=rankingMix, tiempoFinal=tiempo) 

@app.route('/perfil')
def perfil():
  nombre=session['nombre']
  con = sqlite3.connect('base_de_datos.db')
  cur=con.cursor() 
  perfil = []
  tomarRanking = cur.execute(f'''SELECT ranking_musica, tiempo_musica, ranking_libros, tiempo_libros, ranking_cine, tiempo_cine, ranking_mix, tiempo_mix FROM Jugadores WHERE nombre_jugador = "{nombre}"''')
  for x in tomarRanking:
    dicc = {}
    dicc['ranking_musica'] = x[0]
    dicc['tiempo_musica'] = x[1]
    dicc['ranking_libros'] = x[2]
    dicc['tiempo_libros'] = x[3]
    dicc['ranking_cine'] = x[4]
    dicc['tiempo_cine'] = x[5]
    dicc['ranking_mix'] = x[6]
    dicc['tiempo_mix'] = x[7]
    perfil.append(dicc)
  return render_template('perfil.html', nombre=nombre, perfil = perfil)
  
app.run(host='0.0.0.0', port=81)
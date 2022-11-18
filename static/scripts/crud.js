function extraerPreguntas() {
  $.ajax({
    url:"/extraerPreguntas",
    type:"GET",
    success: function(response){
      console.log(response)
      alert("Podes visualizar las preguntas en la consola")
    },
    error: function(error) {
      console.log(error)
    }
  })
}

function extraerRespuestas() {
  $.ajax({
    url:"/extraerRespuestas",
    type:"GET",
    success: function(response){
      console.log(response)
      alert("Podes visualizar las respuestas en la consola")
    },
    error: function(error) {
      console.log(error)
    }
  })
}

//--------------------AGREGAR------------

function agregar(){
  var pregunta = document.getElementById("pregunta").value
  var categoria = document.getElementById("categorias").value
  $.ajax({
    url:"/agregarPregunta",
    type:"POST",
    data:{"preguntaAAgregar":pregunta, "categoriaAAgregar":categoria},
    success: function(response) {
      location.href = "/agregarPreguntas"
      if(response){
        console.log("Pregunta agregada con exito")
        alert("Pregunta agregada con exito")
      } else {
        alert("error")
      }
    },
    error: function(error){
      console.log(error)
    }
  })
}

function agregarRespuesta(){
  var pregunta = document.getElementById("preguntaLista").value
  console.log(pregunta)
  var respuesta = document.getElementById("respuesta").value
  var categoria = document.getElementById("categoria").value
  var esCorrecta = document.getElementById("esCorrecta").value
  var idPregunta = document.getElementById("idPregunta").value
 $.ajax({
    url:"/agregarRespuesta",
    type:"POST",
    data:{"preguntaLista":pregunta, "respuesta":respuesta, "categoria":categoria, "esCorrecta":esCorrecta, "idPregunta":idPregunta},
    success: function(response) {
      location.href = "/agregarPreguntas"
      if(response){
        console.log("Respuesta agregada con exito")
        alert("Respuesta agregada con exito")
      } else {
        alert("error")
      }
    },
    error: function(error){
      console.log(error)
    }
  })
}
//-------------------EDITAR---------------
function editar(){
  var pregunta = document.getElementById("pregunta").value
  print(pregunta)
  var preguntaModificada = document.getElementById("preguntaModificada").value
  print(preguntaModificada)
  $.ajax({
    url:"/editar",
    type:"PUT",
    data:{"pregunta":pregunta, "preguntaModificada":preguntaModificada},
    success: function(response) {
    location.href = "/listaPreguntasEditar"
    console.log(response)
    alert(response)
    respuesta = ""
    },
    error: function(error){
      console.log(error)
    }
  })
}

function editarRespuesta(){
  var respuesta = document.getElementById("respuesta").value
  var respuestaModificada = document.getElementById("respuestaModificada").value
  $.ajax({
    url:"/editarRespuesta",
    type:"PUT",
    data:{"respuesta":respuesta, "respuestaModificada":respuestaModificada},
    success: function(response) {
    location.href = "/listaPreguntasEditar"
    console.log(response)
    alert(response)
    respuesta = ""
    },
    error: function(error){
      console.log(error)
    }
  })
}


//--------------------BORRAR-----------------
function borrarPregunta(){
  var pregunta = document.getElementById("pregunta").value
  console.log(pregunta)
  $.ajax({
    url:"/eliminarPreg",
    type:"DELETE",
    data:{"preguntaAEliminar":pregunta},
    success: function(response) {
    location.href = "/listaPreguntasEliminar"
    console.log(response)
    alert(response)
    },
    error: function(error){
      console.log(error)
    }
  })
}

function borrarRespuesta(){
  var respuesta = document.getElementById("respuesta").value
  $.ajax({
    url:"/eliminarRta",
    type:"DELETE",
    data:{"respuestaAEliminar":respuesta},
    success: function(response) {
    location.href = "/listaPreguntasEliminar"
    console.log(response)
    alert(response)
    },
    error: function(error){
      console.log(error)
    }
  })
}
//-------------------USUARIOS-------------

function extraerUsuarios() {
  $.ajax({
    url:"/extraerUsuarios",
    type:"GET",
    success: function(response){
      console.log(response)
      alert("Podes visualizar los usuarios y sus contraseñas en la consola")
    },
    error: function(error) {
      console.log(error)
    }
  })
}

function borrarUsuario(){
  var usuario = document.getElementById("usuario").value
  console.log(ids)
  $.ajax({
    url:"/eliminarUsuario",
    type:"DELETE",
    data:{"usuarioAEliminar":usuario},
    success: function(response) {
    location.href = "/mostrarUsuariosAEliminar"
    console.log(response)
    alert(response)
    },
    error: function(error){
      console.log(error)
    }
  })
}

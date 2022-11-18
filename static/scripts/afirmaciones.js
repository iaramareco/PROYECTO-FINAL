numAfirmacion = 0;
numRta = 0;
window.onload = mostrarAfirmacion(numAfirmacion);
window.onload = mostrarRta(numRta);
var puntaje = 0;
var tiempo = "!";
var tiempoinicio = (window.onload = Date.now());
//Mostrar la pregunta h2 con imagen

function mostrarAfirmacion(n) {
  s = afirmaciones[n].contenido

  pos_imagen = s.indexOf("imagenes_bdd")
  
  if (pos_imagen != -1) {
      texto = s.substr(0, s.indexOf('https:'))
      s = texto       
      imagen =  afirmaciones[n].contenido.substr(pos_imagen)
      s += '<br><img src="/static/' + imagen + '">';
  } else {
      imagen='....'
  }
    
  document.getElementById('pregunta').innerHTML = s
  console.log(">", imagen)
  
}

//Mostrar afirmación

//Mostrar las rtas en sus botones
function mostrarRta(n) {
  document.getElementById('prim-rta').setAttribute('data-num', `${n}`)
  document.getElementById('prim-rta').innerHTML = respuestas[n][0].contenido_rta
  document.getElementById('seg-rta').setAttribute('data-num', `${n}`)
  document.getElementById('seg-rta').innerHTML = respuestas[n][1].contenido_rta
  document.getElementById('ter-rta').setAttribute('data-num', `${n}`)
  document.getElementById('ter-rta').innerHTML = respuestas[n][2].contenido_rta
  document.getElementById('cuar-rta').setAttribute('data-num', `${n}`)
  document.getElementById('cuar-rta').innerHTML = respuestas[n][3].contenido_rta
}



//boton siguiente
function siguiente() {
    var footer = document.getElementById('footer');
    var contenido = document.getElementById('contenido')
    var botones = document.getElementById('botones')
    var titulo = document.getElementById('titulo');
    var correcto = document.getElementById('correcto');
    var incorrecto = document.getElementById('incorrecto');
    var siguiente = document.getElementById('siguiente');
    contenido.style.display = 'block'; 
    botones.style.display = 'block'; 
    footer.style.display = 'block'; 
    correcto.style.display = 'none'; 
    incorrecto.style.display = 'none';
    siguiente.style.display = 'none';
    var numTitulo = titulo.innerHTML;
    numTitulo++;
    titulo.innerHTML = numTitulo;
    numAfirmacion++;
    mostrarAfirmacion(numAfirmacion);
    numRta++;
    mostrarRta(numRta);
    const categorias =  afirmaciones.map(({ categoria }) => categoria);
    function getOccurrence(categorias, value) {
    var count = 0;
    categorias.forEach((v) => (v === value && count++));
    return count;
    }
    var musica = getOccurrence(categorias, 'Musica');  
    var libros = getOccurrence(categorias, 'Libros');
    var cine = getOccurrence(categorias, 'Cine');
    
  if (numAfirmacion == 11) {
    var elems = document.getElementById("todo");
    elems.style.display='none';
    let cargando = document.querySelector("body");
    let str = '<p>Cargando...</p>';
    cargando.innerHTML = str;
    var tiempofin = (window.onload = Date.now());
    let tiempo = ((tiempofin - tiempoinicio)/1000);
    if (musica == 12) {
      window.location.href = `/finJuegoMusica/${puntaje}/${tiempo}`;
    }
    if (cine == 12) {
       window.location.href =  `/finJuegoCine/${puntaje}/${tiempo}`;
    } 
    if (libros == 12) {
       window.location.href = `/finJuegoLibros/${puntaje}/${tiempo}`;
    } if(libros < 12 && cine < 12 && musica < 12) {
      window.location.href = `/finJuegoMix/${puntaje}/${tiempo}`;
      }
    } 
  }
//---------------------VERIFICAR SI LAS RTAS SON CORRECTAS O NO-----------
function check(n){
  var footer = document.getElementById('footer');
  var contenido = document.getElementById('contenido');
  var botones = document.getElementById('botones');
  var siguiente = document.getElementById('siguiente');
  if((respuestas[n][0].es_correcta == 1)){
    var correcto = document.getElementById('correcto');
    contenido.style.display = 'none'; // desaparece
    botones.style.display = 'none'; //aparece
    footer.style.display = 'none'; //desaparece
    correcto.style.display = 'block'; //aparece
    siguiente.style.display = 'block';
    puntaje++;
  }else{
    var incorrecto = document.getElementById('incorrecto');
    contenido.style.display = 'none';
    footer.style.display = 'none';
    incorrecto.style.display = 'block';
    siguiente.style.display = 'block';
  }  
  }

function check2(n){
  var footer = document.getElementById('footer');
  var contenido = document.getElementById('contenido');
  var botones = document.getElementById('botones');
  var siguiente = document.getElementById('siguiente');
  if((respuestas[n][1].es_correcta == 1)){
    var correcto = document.getElementById('correcto');
    contenido.style.display = 'none'; // desaparece
    botones.style.display = 'block'; //aparece
    footer.style.display = 'none'; //desaparece
    correcto.style.display = 'block'; //aparece
    siguiente.style.display = 'block';
    puntaje++;
  }else{
    var incorrecto = document.getElementById('incorrecto');
    contenido.style.display = 'none';
    footer.style.display = 'none';
    incorrecto.style.display = 'block';
    siguiente.style.display = 'block';
    check2(numRta);
  }  
  }

function check3(n){
  var footer = document.getElementById('footer');
  var contenido = document.getElementById('contenido');
  var botones = document.getElementById('botones');
  var siguiente = document.getElementById('siguiente');
  if((respuestas[n][2].es_correcta == 1)){
    var correcto = document.getElementById('correcto');
    contenido.style.display = 'none'; // desaparece
    botones.style.display = 'block'; //desaparece
    footer.style.display = 'none'; //desaparece
    correcto.style.display = 'block'; //aparece
    siguiente.style.display = 'block';
    puntaje++;
  }else{
    var incorrecto = document.getElementById('incorrecto');
    contenido.style.display = 'none';
    footer.style.display = 'none';
    incorrecto.style.display = 'block';
    siguiente.style.display = 'block';
  }  
  }

function check4(n){
  var footer = document.getElementById('footer');
  var contenido = document.getElementById('contenido');
  var botones = document.getElementById('botones');
  var siguiente = document.getElementById('siguiente');
  if((respuestas[n][3].es_correcta == 1)){
    var correcto = document.getElementById('correcto');
    contenido.style.display = 'none'; // desaparece
    botones.style.display = 'block'; //desaparece
    footer.style.display = 'none'; //desaparece
    correcto.style.display = 'block'; //aparece
    siguiente.style.display = 'block';
    puntaje++;
  }else{
    var incorrecto = document.getElementById('incorrecto');
    contenido.style.display = 'none';
    footer.style.display = 'none';
    incorrecto.style.display = 'block';
    siguiente.style.display = 'block';
  }  
  }




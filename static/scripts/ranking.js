window.onload = function mostrarRanking() { 
document.getElementById('nombre').innerHTML = ranking[0].nombre;
document.getElementById('ranking').innerHTML = ranking[0].ranking_musica;
document.getElementById('tiempo').innerHTML = ranking[0].tiempo_musica;
document.getElementById('nombre2').innerHTML = ranking[1].nombre;
document.getElementById('ranking2').innerHTML = ranking[1].ranking_musica;
document.getElementById('tiempo2').innerHTML = ranking[1].tiempo_musica;
document.getElementById('nombre3').innerHTML = ranking[2].nombre;
document.getElementById('ranking3').innerHTML = ranking[2].ranking_musica;
document.getElementById('tiempo3').innerHTML = ranking[2].tiempo_musica;
}


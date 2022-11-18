window.onload = function mostrarRanking() { 
document.getElementById('puntaje1').innerHTML = perfil[0].ranking_musica;
document.getElementById('tiempo1').innerHTML = perfil[0].tiempo_musica;
document.getElementById('puntaje2').innerHTML = perfil[0].ranking_cine;
document.getElementById('tiempo2').innerHTML = perfil[0].tiempo_cine;
document.getElementById('puntaje3').innerHTML = perfil[0].ranking_libros;
document.getElementById('tiempo3').innerHTML = perfil[0].tiempo_libros;
document.getElementById('puntaje4').innerHTML = perfil[0].ranking_mix;
document.getElementById('tiempo4').innerHTML = perfil[0].tiempo_mix;
}


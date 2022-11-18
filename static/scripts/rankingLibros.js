window.onload = function mostrarRankingLibros() { 
document.getElementById('nombreLibros').innerHTML = rankingLibros[0].nombre;
document.getElementById('rankingLibros').innerHTML = rankingLibros[0].ranking_libros;
document.getElementById('tiempoLibros').innerHTML = rankingLibros[0].tiempo_libros;
document.getElementById('nombreLibros2').innerHTML = rankingLibros[1].nombre;
document.getElementById('rankingLibros2').innerHTML = rankingLibros[1].ranking_libros;
document.getElementById('tiempoLibros2').innerHTML = rankingLibros[1].tiempo_libros;
document.getElementById('nombreLibros3').innerHTML = rankingLibros[2].nombre;
document.getElementById('rankingLibros3').innerHTML = rankingLibros[2].ranking_libros;
document.getElementById('tiempoLibros3').innerHTML = rankingLibros[2].tiempo_libros;
}


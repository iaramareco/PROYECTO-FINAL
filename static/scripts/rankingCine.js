window.onload = function mostrarRankingCine() { 
document.getElementById('nombreCine').innerHTML = rankingCine[0].nombre;
document.getElementById('rankingCine').innerHTML = rankingCine[0].ranking_cine;
document.getElementById('tiempoCine').innerHTML = rankingCine[0].tiempo_cine;
document.getElementById('nombreCine2').innerHTML = rankingCine[1].nombre;
document.getElementById('rankingCine2').innerHTML = rankingCine[1].ranking_cine;
document.getElementById('tiempoCine2').innerHTML = rankingCine[1].tiempo_cine;
document.getElementById('nombreCine3').innerHTML = rankingCine[2].nombre;
document.getElementById('rankingCine3').innerHTML = rankingCine[2].ranking_cine;
document.getElementById('tiempoCine3').innerHTML = rankingCine[2].tiempo_cine;
}


function bloquearSlot(fecha, hora) {
    document.getElementById('blockFecha').value = fecha;
    document.getElementById('blockHora').value = hora;
    document.getElementById('blockModal').style.display = 'block';
}

function cerrarModal() {
    document.getElementById('blockModal').style.display = 'none';
}

// Cerrar modal al hacer clic fuera
window.onclick = function(event) {
    const modal = document.getElementById('blockModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}
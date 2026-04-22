document.addEventListener('DOMContentLoaded', function() {
    // 1. Buscamos todas las alertas que existan en la página
    const alertas = document.querySelectorAll('.alerta');

    alertas.forEach(function(alerta) {
        // 2. Esperar 3 segundos (3000ms) quieto
        setTimeout(function() {
            // Aplicamos el efecto de desvanecimiento
            alerta.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            alerta.style.opacity = "0";
            alerta.style.transform = "translateY(-20px)";
            
            // 3. Esperar 0.5s más (mientras termina la animación) para borrarlo
            setTimeout(function() {
                alerta.remove();
            }, 500);
            
        }, 3000); 
    });
});
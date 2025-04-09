const API_HOME_URL = "http://localhost:8001/home"; 
const API_CARRITO_URL = "http://localhost:8004/carrito/agregar"; 
const token = JSON.parse(localStorage.getItem('usuario'))?.token; 


function actualizarBotonSesion() {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  const botonSesion = document.getElementById('boton-sesion');
  const nombreUsuario = document.getElementById('nombre-usuario');

  if (usuario?.token) {
    botonSesion.textContent = "Cerrar sesión";
    botonSesion.href = "#";
    botonSesion.addEventListener('click', (e) => {
      e.preventDefault();
      localStorage.removeItem('usuario');
      window.location.reload();
    });

    if (usuario.username) {
      nombreUsuario.textContent = `Hola, ${usuario.username}`;
    }
  } else {
    botonSesion.textContent = "Iniciar sesión";
    botonSesion.href = "./login.html";
    nombreUsuario.textContent = "";
  }
}

actualizarBotonSesion();

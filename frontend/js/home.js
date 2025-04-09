const API_HOME_URL = "http://localhost:8001/home"; 
const API_CARRITO_URL = "http://localhost:8004/carrito/agregar"; 
const token = JSON.parse(localStorage.getItem('usuario'))?.token; 

let librosGlobal = []; 

async function cargarLibros() {
  try {
    const response = await fetch(API_HOME_URL);
    if (!response.ok) {
      throw new Error('Error al obtener los libros: ' + response.statusText);
    }
    const data = await response.json();
    const libros = data.libros_mas_vendidos;
    librosGlobal = libros; 

    const contenedor = document.getElementById('libros-container');
    contenedor.innerHTML = '';

    libros.forEach((libro, index) => {
      const tarjeta = document.createElement('div');
      tarjeta.className = 'libro-card';

      tarjeta.innerHTML = `
        <img src="${libro.imagen}" alt="${libro.titulo}" style="width:100px; height:150px; margin-bottom:10px;">
        <h2>${libro.titulo}</h2>
        <p>${libro.descripcion}</p>
        <p class="precio">$${parseFloat(libro.precio_total).toFixed(2)}</p>
        <button class="agregar-btn" onclick="agregarAlCarrito(${index})">Agregar al Carrito</button>
      `;

      contenedor.appendChild(tarjeta);
    });
  } catch (error) {
    console.error('Error al cargar los libros:', error);
  }
}

async function agregarAlCarrito(indiceLibro) {
  if (!token) {
    alert("Debes iniciar sesión primero.");
    window.location.href = "./login.html";
    return;
  }

  const libro = librosGlobal[indiceLibro];
  console.log("Libro seleccionado:", libro); 

  if (!libro?.id) {
    alert("Este libro no tiene un ID válido.");
    return;
  }

  const cantidad = prompt(`¿Cuántos deseas agregar de "${libro.titulo}"?`);
  if (cantidad && parseInt(cantidad) > 0) {
    try {
      const response = await fetch(API_CARRITO_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          libro_id: libro.id, 
          cantidad: parseInt(cantidad)
        })
      });

      const data = await response.json();

      if (response.ok) {
        alert("Producto agregado al carrito");
      } else {
        const detalle = typeof data.detail === "object" ? JSON.stringify(data.detail) : data.detail;
        alert(detalle || "Error al agregar al carrito");
      }
    } catch (error) {
      console.error('Error al agregar al carrito:', error);
      alert("Error de conexión con el microservicio de carrito");
    }
  }
}



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

    // Mostrar nombre de usuario
    if (usuario.username) {
      nombreUsuario.textContent = `Hola, ${usuario.username}`;
    }
  } else {
    botonSesion.textContent = "Iniciar sesión";
    botonSesion.href = "./login.html";
    nombreUsuario.textContent = "";
  }
}

cargarLibros();
actualizarBotonSesion();

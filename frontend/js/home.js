const API_HOME_URL = "http://localhost:8001/home"; // Microservicio Home
const API_CARRITO_URL = "http://localhost:8004/carrito/agregar"; // Microservicio Carrito
const token = JSON.parse(localStorage.getItem('usuario'))?.token; // Leer token guardado

let librosGlobal = []; // Guardar los libros

async function cargarLibros() {
  try {
    const response = await fetch(API_HOME_URL);
    if (!response.ok) {
      throw new Error('Error al obtener los libros: ' + response.statusText);
    }
    const data = await response.json();
    const libros = data.libros_mas_vendidos;
    librosGlobal = libros; // Guardar libros para usarlos al agregar

    const contenedor = document.getElementById('libros-container');
    contenedor.innerHTML = '';

    libros.forEach((libro, index) => {
      const tarjeta = document.createElement('div');
      tarjeta.className = 'libro-card';

      tarjeta.innerHTML = `
        <img src="assets/images/default_book.png" alt="Libro" style="width:100px; height:150px; margin-bottom:10px;">
        <h2>${libro.titulo}</h2>
        <p>${libro.descripcion}</p>
        <p class="precio">$${libro.precio_total.toFixed(2)}</p>
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
    window.location.href = "/login.html";
    return;
  }

  const libro = librosGlobal[indiceLibro];
  const cantidad = prompt(`¿Cuántos deseas agregar de "${libro.titulo}"?`);
  if (cantidad && cantidad > 0) {
    try {
      const response = await fetch(API_CARRITO_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          libro_id: libro.id,  // Recuerda que el libro necesita su id
          cantidad: parseInt(cantidad)
        })
      });

      const data = await response.json();

      if (response.ok) {
        alert("Producto agregado al carrito ✅");
      } else {
        alert(data.detail || "Error al agregar al carrito");
      }
    } catch (error) {
      console.error('Error al agregar al carrito:', error);
    }
  }
}

cargarLibros();

const API_CATEGORIAS_URL = "http://localhost:8003/categorias";
const API_CARRITO_URL = "http://localhost:8004/carrito/agregar";
const token = JSON.parse(localStorage.getItem('usuario'))?.token;

let categoriasGlobal = [];

async function cargarCategorias() {
  try {
    const response = await fetch(API_CATEGORIAS_URL);
    const data = await response.json();

    categoriasGlobal = data;
    const select = document.getElementById("categoria-select");

    data.forEach((categoria, index) => {
      const option = document.createElement("option");
      option.value = index;
      option.textContent = categoria.categoria;
      select.appendChild(option);
    });

    select.addEventListener("change", () => mostrarLibrosPorCategoria(select.value));
  } catch (error) {
    console.error("Error al cargar categorías:", error);
  }
}

function mostrarLibrosPorCategoria(indice) {
  const contenedor = document.getElementById("libros-categoria-container");
  contenedor.innerHTML = "";

  if (!categoriasGlobal[indice]) return;

  const libros = categoriasGlobal[indice].libros;

  libros.forEach((libro, i) => {
    const tarjeta = document.createElement("div");
    tarjeta.className = "libro-card";

    tarjeta.innerHTML = `
      <img src="${libro.imagen}" alt="${libro.titulo}" style="width:100px; height:150px; margin-bottom:10px;">
      <h2>${libro.titulo}</h2>
      <p>${libro.descripcion}</p>
      <p class="precio">$${parseFloat(libro.precio_con_iva).toFixed(2)}</p>
      <button class="agregar-btn" onclick="agregarAlCarritoDesdeCategoria(${indice}, ${i})">
        Agregar al Carrito
      </button>
    `;

    contenedor.appendChild(tarjeta);
  });
}

async function agregarAlCarritoDesdeCategoria(indiceCategoria, indiceLibro) {
  if (!token) {
    alert("Debes iniciar sesión primero.");
    window.location.href = "./login.html";
    return;
  }

  const libro = categoriasGlobal[indiceCategoria]?.libros[indiceLibro];
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

    if (usuario.username) {
      nombreUsuario.textContent = `Hola, ${usuario.username}`;
    }
  } else {
    botonSesion.textContent = "Iniciar sesión";
    botonSesion.href = "./login.html";
    nombreUsuario.textContent = "";
  }
}

cargarCategorias();
actualizarBotonSesion();

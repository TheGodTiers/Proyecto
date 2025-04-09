const API_URL = "http://localhost:8000";
const token = localStorage.getItem("token"); // Asumo que guardaste el token en localStorage al iniciar sesión

if (!token) {
  alert("Debes iniciar sesión primero.");
  window.location.href = "/login.html"; // Redirigir al login si no hay token
}

async function cargarCarrito() {
  const res = await fetch(`${API_URL}/carrito`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const data = await res.json();
  
  const carritoDiv = document.getElementById("carrito-lista");
  carritoDiv.innerHTML = ""; // Limpiar

  if (data.carrito.length === 0) {
    carritoDiv.innerHTML = "<p>Tu carrito está vacío 🛒</p>";
  } else {
    data.carrito.forEach(item => {
      const itemDiv = document.createElement("div");
      itemDiv.className = "carrito-item";

      itemDiv.innerHTML = `
        <h3>${item.titulo}</h3>
        <p>Cantidad: ${item.cantidad}</p>
        <p>Precio Total: $${item.precio_total.toFixed(2)}</p>
        <div class="acciones">
          <button onclick="editarCantidad(${item.libro_id})">Editar</button>
          <button onclick="eliminarProducto(${item.libro_id})">Eliminar</button>
        </div>
      `;

      carritoDiv.appendChild(itemDiv);
    });
  }

  document.getElementById("total-precio").textContent = data.precio_final;
}

async function editarCantidad(libroId) {
  const nuevaCantidad = prompt("¿Nueva cantidad?");
  if (nuevaCantidad && nuevaCantidad > 0) {
    await fetch(`${API_URL}/carrito/editar`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ libro_id: libroId, nueva_cantidad: parseInt(nuevaCantidad) })
    });
    cargarCarrito();
  }
}

async function eliminarProducto(libroId) {
  if (confirm("¿Seguro que deseas eliminar este producto?")) {
    await fetch(`${API_URL}/carrito/eliminar`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ libro_id: libroId })
    });
    cargarCarrito();
  }
}

async function realizarCompra() {
  if (confirm("¿Deseas realizar la compra?")) {
    const res = await fetch(`${API_URL}/carrito/realizar_compra`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    const data = await res.json();
    alert(`¡Compra realizada! ID Pedido: ${data.pedido_id}\nTotal: $${data.total}`);
    cargarCarrito(); // Recargar carrito vacío
  }
}

document.getElementById("comprar-btn").addEventListener("click", realizarCompra);

// Cargar carrito al iniciar
cargarCarrito();

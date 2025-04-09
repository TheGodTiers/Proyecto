const API_CARRITO_URL = "http://localhost:8004/carrito";
const API_EDITAR_URL = "http://localhost:8004/carrito/editar";
const API_ELIMINAR_URL = "http://localhost:8004/carrito/eliminar";
const API_COMPRA_URL = "http://localhost:8004/carrito/realizar_compra";

const token = JSON.parse(localStorage.getItem("usuario"))?.token;

async function cargarCarrito() {
  if (!token) {
    alert("Debes iniciar sesión primero");
    window.location.href = "./login.html";
    return;
  }

  try {
    const response = await fetch(API_CARRITO_URL, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error("Fallo al obtener el carrito");
    }

    const data = await response.json();
    const { carrito, precio_final } = data;

    const contenedor = document.getElementById("carrito-container");
    const resumen = document.querySelector(".resumen-compra");
    contenedor.innerHTML = "";

    if (carrito.length === 0) {
      contenedor.innerHTML = "<p>No tienes productos en el carrito.</p>";
      resumen.innerHTML = "";
      return;
    }

    carrito.forEach(item => {
      const tarjeta = document.createElement("div");
      tarjeta.className = "libro-card";
      tarjeta.innerHTML = `
        <img src="${item.imagen || './placeholder.jpg'}" alt="${item.titulo}" style="width:100px; height:150px;">
        <h3>${item.titulo}</h3>
        <p>Total: $${item.precio_total.toFixed(2)}</p>
        <input type="number" min="1" value="${item.cantidad}" onchange="editarCantidad(${item.libro_id}, this.value)" />
        <button onclick="eliminarProducto(${item.libro_id})">Eliminar</button>
      `;
      contenedor.appendChild(tarjeta);
    });

    resumen.innerHTML = `
      <h2>Resumen de Compra</h2>
      <p><strong>Total:</strong> $${precio_final.toFixed(2)}</p>
      <button onclick="realizarCompra()">Finalizar Compra</button>
    `;
  } catch (error) {
    console.error("Error al cargar el carrito:", error);
    alert("No se pudo cargar el carrito.");
  }
}

async function editarCantidad(libroId, nuevaCantidad) {
  try {
    await fetch(API_EDITAR_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        libro_id: libroId,
        nueva_cantidad: parseInt(nuevaCantidad)
      })
    });
    cargarCarrito();
  } catch (error) {
    console.error("Error al editar cantidad:", error);
  }
}

async function eliminarProducto(libroId) {
  try {
    await fetch(API_ELIMINAR_URL, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ libro_id: libroId })
    });
    cargarCarrito();
  } catch (error) {
    console.error("Error al eliminar producto:", error);
  }
}

async function realizarCompra() {
  try {
    const response = await fetch(API_COMPRA_URL, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const data = await response.json();

    if (response.ok) {
      alert(`Compra realizada exitosamente. ID del pedido: ${data.pedido_id}`);
      cargarCarrito();
    } else {
      alert(data.detail || "Error al realizar la compra.");
    }
  } catch (error) {
    console.error("Error al realizar compra:", error);
  }
}

cargarCarrito();

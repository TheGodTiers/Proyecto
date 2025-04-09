const API_PEDIDOS_URL = "http://localhost:8005/pedidos"; // Microservicio de pedidos
const token = JSON.parse(localStorage.getItem('usuario'))?.token;

async function cargarPedidos() {
  if (!token) {
    alert("Debes iniciar sesión primero.");
    window.location.href = "/login.html";
    return;
  }

  try {
    const response = await fetch(API_PEDIDOS_URL, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (response.status === 403) {
      alert("Acceso denegado: Solo los administradores pueden ver esta sección.");
      window.location.href = "/index.html";
      return;
    }

    if (!response.ok) {
      throw new Error('Error al obtener los pedidos');
    }

    const pedidos = await response.json();
    const contenedor = document.getElementById('pedidos-container');
    contenedor.innerHTML = '';

    if (pedidos.length === 0) {
      contenedor.innerHTML = '<p>No hay pedidos realizados.</p>';
      return;
    }

    pedidos.forEach(pedido => {
      const pedidoDiv = document.createElement('div');
      pedidoDiv.className = 'pedido';

      let detallesHTML = '';
      pedido.detalles.forEach(detalle => {
        detallesHTML += `
          <div class="detalles">
            <p><strong>${detalle.titulo}</strong></p>
            <p>Cantidad: ${detalle.cantidad}</p>
            <p>Precio unitario: $${detalle.precio_unitario.toFixed(2)}</p>
            <p>IVA: $${detalle.iva.toFixed(2)}</p>
          </div>
          <hr>
        `;
      });

      pedidoDiv.innerHTML = `
        <h2>Pedido #${pedido.pedido_id}</h2>
        <p><strong>Usuario ID:</strong> ${pedido.usuario_id}</p>
        <p><strong>Fecha:</strong> ${pedido.fecha}</p>
        <p><strong>Total:</strong> $${pedido.total.toFixed(2)}</p>
        ${detallesHTML}
      `;

      contenedor.appendChild(pedidoDiv);
    });

  } catch (error) {
    console.error('Error al cargar pedidos:', error);
  }
}

cargarPedidos();

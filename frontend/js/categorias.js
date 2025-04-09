async function cargarCategorias() {
    try {
      const response = await fetch('http://localhost:8003/categorias');
      if (!response.ok) {
        throw new Error('Error al obtener categorías: ' + response.statusText);
      }
      const categorias = await response.json();
      const contenedor = document.getElementById('categorias-container');
  
      categorias.forEach(categoria => {
        const tarjeta = document.createElement('div');
        tarjeta.className = 'categoria-card';
  
        // Título de la categoría
        let html = `<h2>${categoria.categoria}</h2>`;
  
        // Si hay libros en la categoría, los mostramos
        if (categoria.libros && categoria.libros.length > 0) {
          html += '<ul>';
          categoria.libros.forEach(libro => {
            html += `
              <li>
                <strong>${libro.titulo}</strong><br>
                ${libro.descripcion}<br>
                <span class="precio">$${libro.precio_con_iva.toFixed(2)}</span>
              </li>
            `;
          });
          html += '</ul>';
        } else {
          html += '<p>No hay libros en esta categoría.</p>';
        }
  
        tarjeta.innerHTML = html;
        contenedor.appendChild(tarjeta);
      });
    } catch (error) {
      console.error('Error al cargar categorías:', error);
    }
  }
  
  // Cargar las categorías al iniciar la página
  cargarCategorias();
  
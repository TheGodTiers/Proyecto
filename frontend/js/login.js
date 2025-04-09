const form = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  const formData = new URLSearchParams();
  formData.append('username', username);
  formData.append('password', password);

  try {
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: formData
    });

    const data = await response.json();

    if (response.ok && data.access_token) {
      const token = data.access_token;
      const payloadBase64 = token.split('.')[1];
      const decodedPayload = JSON.parse(atob(payloadBase64));
      const rol = decodedPayload.rol;

      localStorage.setItem('usuario', JSON.stringify({
        username: username,
        token: token,
        rol: rol
      }));

      if (rol === "admin") {
        window.location.href = "admin.html";
      } else {
        window.location.href = "home.html";
      }
    } else {
      errorMessage.textContent = data.detail || "Error al iniciar sesión";
    }

  } catch (error) {
    console.error('Error en login:', error);
    errorMessage.textContent = "Error de conexión";
  }
});

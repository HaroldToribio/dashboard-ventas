const API = "http://127.0.0.1:5000";

// MENU
document.getElementById("menu-toggle").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("active");
});

// NAVEGACIÓN
function mostrarSeccion(id) {
  document.querySelectorAll(".seccion").forEach(sec => {
    sec.classList.remove("activa");
  });

  document.getElementById(id).classList.add("activa");
}

// =========================
// 📊 DASHBOARD
// =========================

let graficaPrincipal = null;

async function cargarVentas() {
  try {
    const res = await fetch(`${API}/ventas-por-producto`);
    const data = await res.json();

    const labels = data.map(p => p.nombre);
    const valores = data.map(p => parseFloat(p.total));

    if (valores.length > 0) {
      const total = valores.reduce((a, b) => a + b, 0);
      const promedio = total / valores.length;

      document.getElementById("totalVentas").innerText = `$` + total.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      document.getElementById("promedioVentas").innerText = `$` + promedio.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    }

    if (graficaPrincipal) {
      graficaPrincipal.destroy();
    }

    graficaPrincipal = new Chart(document.getElementById("graficaVentas"), {
      type: "pie",
      data: {
        labels: labels,
        datasets: [{
          label: "Ventas por Producto",
          data: valores
        }]
      },
      options: {
        plugins: {
          legend: {
            labels: { color: "#fff" }
          }
        }
      }
    });

  } catch (error) {
    console.error("Error cargando ventas:", error);
  }
}

// =========================
// 📦 PRODUCTOS
// =========================

async function cargarProductos() {
  const res = await fetch(`${API}/productos`);
  const data = await res.json();

  const lista = document.getElementById("lista-productos");
  lista.innerHTML = "";

  data.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = `${p.nombre} - $${p.precio}`;
    lista.appendChild(li);
  });

  document.getElementById("totalProductos").innerText = data.length;
}

document.getElementById("form-producto").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nombre = document.getElementById("nombre").value;
  const precio = parseFloat(document.getElementById("precio").value);

  try {
    const res = await fetch(`${API}/productos`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ nombre, precio })
    });

    if (!res.ok) {
      const error = await res.text();
      alert("Error backend: " + error);
      return;
    }

    document.getElementById("form-producto").reset();

    await cargarProductos();
    await cargarResumenProductos();

  } catch (err) {
    console.error(err);
  }
});

// =========================
// 📈 REPORTES
// =========================

async function cargarProductosGrafica() {
  try {
    const res = await fetch(`${API}/ventas-por-producto`);
    const data = await res.json();

    const labels = data.map(p => p.nombre);
    const valores = data.map(p => p.total);

    new Chart(document.getElementById("graficaProductos"), {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Ventas por Producto",
          data: valores
        }]
      }
    });

  } catch (error) {
    console.error("Error grafica productos:", error);
  }
}

// =========================
// 💰 RESUMEN PRODUCTOS
// =========================

let graficoMini = null;

async function cargarResumenProductos() {
  const res = await fetch(`${API}/ventas`);
  const data = await res.json();

  let total = data.reduce((sum, v) => sum + parseFloat(v.total), 0);

  document.getElementById("totalVentasProductos").innerText = "$" + total.toFixed(2);

  const labels = data.map(v => v.fecha);
  const valores = data.map(v => v.total);

  // 🔥 evitar duplicar grafica
  if (graficoMini) {
    graficoMini.destroy();
  }

  graficoMini = new Chart(document.getElementById("graficoMini"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Ventas",
        data: valores
      }]
    }
  });
}

// =========================
// 🧠 RESUMEN GLOBAL (ARREGLADO)
// =========================

async function cargarResumen() {
  const res = await fetch(`${API}/ventas`);
  const data = await res.json();

  let total = data.reduce((sum, v) => sum + parseFloat(v.total), 0);

  document.getElementById("totalVentas").innerText = "$" + total.toFixed(2);
}

async function cargarDashboardResumen() {
  try {
    const res = await fetch(`${API}/dashboard?producto=1&dias=7`);
    const data = await res.json();

    console.log("Dashboard:", data);

    // Puedes mostrarlo donde ya tienes el resumen
    document.getElementById("totalVentas").innerText =
      "$" + parseFloat(data.total_ventas || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

    document.getElementById("promedioVentas").innerText =
      "$" + parseFloat(data.promedio_ventas || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  } catch (error) {
    console.error("Error dashboard:", error);
  }
}

// =========================
// 🚀 INIT
// =========================

cargarVentas();
cargarProductos();
cargarProductosGrafica();
cargarResumenProductos();
cargarResumen();
cargarDashboardResumen();
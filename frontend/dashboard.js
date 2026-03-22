const API = "http://127.0.0.1:5000";

// ─────────────────────────────────────────
// MENU & NAVEGACIÓN
// ─────────────────────────────────────────

document.getElementById("menu-toggle").addEventListener("click", () => {
  document.getElementById("sidebar").classList.toggle("active");
});

function mostrarSeccion(id) {
  document.querySelectorAll(".seccion").forEach(sec => sec.classList.remove("activa"));
  document.getElementById(id).classList.add("activa");
}

// ─────────────────────────────────────────
// DASHBOARD PRINCIPAL
// ─────────────────────────────────────────

let graficaPrincipal = null;

async function cargarDashboardResumen() {
  try {
    const res  = await fetch(`${API}/dashboard?producto=1&dias=7`);
    const data = await res.json();

    document.getElementById("totalVentas").innerText =
      "$" + parseFloat(data.total_ventas || 0).toLocaleString("en-US", { minimumFractionDigits: 2 });
    document.getElementById("promedioVentas").innerText =
      "$" + parseFloat(data.promedio_ventas || 0).toLocaleString("en-US", { minimumFractionDigits: 2 });
    document.getElementById("totalProductosDash").innerText = data.total_productos || 0;
    document.getElementById("productoTop").innerText = data.producto_top || "—";

  } catch (err) {
    console.error("Error dashboard resumen:", err);
  }
}

async function cargarVentas() {
  try {
    const res  = await fetch(`${API}/ventas-por-producto`);
    const data = await res.json();

    const labels  = data.map(p => p.nombre);
    const valores = data.map(p => parseFloat(p.total));

    if (graficaPrincipal) graficaPrincipal.destroy();

    graficaPrincipal = new Chart(document.getElementById("graficaVentas"), {
      type: "pie",
      data: {
        labels,
        datasets: [{
          label: "Ventas por Producto ($)",
          data: valores,
          backgroundColor: ["#6c63ff", "#48cfad", "#fc6e51", "#a0d468", "#ffce54"]
        }]
      },
      options: {
        plugins: {
          legend: { labels: { color: "#ccc" } }
        }
      }
    });

  } catch (err) {
    console.error("Error cargando ventas:", err);
  }
}

// ─────────────────────────────────────────
// PRODUCTOS
// ─────────────────────────────────────────

async function cargarProductos() {
  const res  = await fetch(`${API}/productos`);
  const data = await res.json();

  const lista = document.getElementById("lista-productos");
  lista.innerHTML = "";

  data.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${p.nombre} — $${parseFloat(p.precio).toFixed(2)}</span>
      <button class="btn-delete" onclick="eliminarProducto(${p.id_producto})">🗑</button>
    `;
    lista.appendChild(li);
  });

  document.getElementById("totalProductos").innerText = data.length;

  // Llenar select de predicción con los mismos productos
  const select = document.getElementById("selectProducto");
  select.innerHTML = "";
  data.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.id_producto;
    opt.textContent = p.nombre;
    select.appendChild(opt);
  });
}

document.getElementById("form-producto").addEventListener("submit", async (e) => {
  e.preventDefault();

  const nombre          = document.getElementById("nombre").value;
  const precio          = parseFloat(document.getElementById("precio").value);
  const promedio_ventas = parseInt(document.getElementById("promedio_ventas").value);

  try {
    const res = await fetch(`${API}/productos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nombre, precio, promedio_ventas })
    });

    if (!res.ok) {
      const err = await res.text();
      alert("Error: " + err);
      return;
    }

    document.getElementById("form-producto").reset();

    await cargarProductos();
    await cargarResumenProductos();
    await cargarVentas();
    await cargarDashboardResumen();

  } catch (err) {
    console.error(err);
  }
});

async function eliminarProducto(id) {
  if (!confirm("¿Eliminar este producto y sus ventas?")) return;

  await fetch(`${API}/productos/${id}`, { method: "DELETE" });
  await cargarProductos();
  await cargarResumenProductos();
  await cargarDashboardResumen();
  await cargarVentas();
}

// ─────────────────────────────────────────
// RESUMEN LATERAL (sección Productos)
// ─────────────────────────────────────────

let graficoMini = null;

async function cargarResumenProductos() {
  const res  = await fetch(`${API}/ventas`);
  const data = await res.json();

  const total = data.reduce((sum, v) => sum + parseFloat(v.total), 0);
  document.getElementById("totalVentasProductos").innerText = "$" + total.toFixed(2);

  const labels  = data.slice(0, 10).map(v => v.fecha);
  const valores = data.slice(0, 10).map(v => parseFloat(v.total));

  if (graficoMini) graficoMini.destroy();

  graficoMini = new Chart(document.getElementById("graficoMini"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Ventas ($)",
        data: valores,
        backgroundColor: "#6c63ff"
      }]
    },
    options: {
      plugins: { legend: { labels: { color: "#ccc" } } },
      scales: {
        x: { ticks: { color: "#ccc", maxRotation: 45 } },
        y: { ticks: { color: "#ccc" } }
      }
    }
  });
}

// ─────────────────────────────────────────
// REPORTES
// ─────────────────────────────────────────

let graficaReportes = null;

async function cargarProductosGrafica() {
  try {
    const res  = await fetch(`${API}/ventas-por-producto`);
    const data = await res.json();

    const labels  = data.map(p => p.nombre);
    const valores = data.map(p => parseFloat(p.total));

    if (graficaReportes) graficaReportes.destroy();

    graficaReportes = new Chart(document.getElementById("graficaProductos"), {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Ventas Totales por Producto ($)",
          data: valores,
          backgroundColor: ["#6c63ff", "#48cfad", "#fc6e51"]
        }]
      },
      options: {
        plugins: { legend: { labels: { color: "#ccc" } } },
        scales: {
          x: { ticks: { color: "#ccc" } },
          y: { ticks: { color: "#ccc" } }
        }
      }
    });

  } catch (err) {
    console.error("Error reportes:", err);
  }
}

// ─────────────────────────────────────────
// PREDICCIÓN ML
// ─────────────────────────────────────────

let graficaPrediccion = null;

async function cargarPrediccion() {
  const productoId = document.getElementById("selectProducto").value;
  const dias       = document.getElementById("selectDias").value;

  if (!productoId) { alert("Selecciona un producto"); return; }

  document.getElementById("prediccion-resultado").style.display = "none";
  document.getElementById("prediccion-loading").style.display  = "block";

  try {
    const res  = await fetch(`${API}/prediccion/${productoId}?dias=${dias}`);
    const data = await res.json();

    document.getElementById("prediccion-loading").style.display = "none";

    if (data.error) {
      alert("Error: " + data.error);
      return;
    }

    // ── Estadísticas históricas ──────────────
    document.getElementById("modeloUsado").innerText  = data.modelo_seleccionado || "—";
    document.getElementById("histPromedio").innerText = data.estadisticas_historicas.promedio_diario + " uds/día";
    document.getElementById("histTotal").innerText    = data.estadisticas_historicas.total_vendido   + " uds";
    document.getElementById("histDias").innerText     = data.estadisticas_historicas.dias_registrados;

    // ── Tabla comparación de modelos ─────────
    const comparacion = data.comparacion_modelos;
    let html = `<table class="tabla-modelos">
      <thead><tr><th>Modelo</th><th>MAE ↓</th><th>R² ↑</th><th></th></tr></thead><tbody>`;

    for (const [nombre, metricas] of Object.entries(comparacion)) {
      const esMejor = nombre === data.modelo_seleccionado;
      html += `<tr class="${esMejor ? 'mejor-modelo' : ''}">
        <td>${nombre}</td>
        <td>${metricas.MAE !== null ? metricas.MAE : "—"}</td>
        <td>${metricas.R2  !== null ? metricas.R2  : "—"}</td>
        <td>${esMejor ? "✅ Seleccionado" : ""}</td>
      </tr>`;
    }
    html += "</tbody></table>";
    document.getElementById("tablaModelos").innerHTML = html;

    // ── Gráfica de predicciones ───────────────
    const fechas = data.predicciones.map(p => p.fecha);
    const preds  = data.predicciones.map(p => p.prediccion);

    if (graficaPrediccion) graficaPrediccion.destroy();

    graficaPrediccion = new Chart(document.getElementById("graficaPrediccion"), {
      type: "line",
      data: {
        labels: fechas,
        datasets: [{
          label: "Demanda Predicha (unidades)",
          data: preds,
          borderColor: "#6c63ff",
          backgroundColor: "rgba(108,99,255,0.15)",
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointBackgroundColor: "#6c63ff"
        }]
      },
      options: {
        plugins: {
          legend: { labels: { color: "#ccc" } },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.parsed.y.toFixed(1)} unidades`
            }
          }
        },
        scales: {
          x: { ticks: { color: "#ccc" } },
          y: {
            ticks: { color: "#ccc" },
            title: { display: true, text: "Unidades", color: "#aaa" }
          }
        }
      }
    });

    document.getElementById("prediccion-resultado").style.display = "block";

  } catch (err) {
    document.getElementById("prediccion-loading").style.display = "none";
    console.error("Error predicción:", err);
    alert("No se pudo obtener la predicción.");
  }
}

// ─────────────────────────────────────────
// INIT
// ─────────────────────────────────────────

(async () => {
  await cargarDashboardResumen();
  await cargarVentas();
  await cargarProductos();
  await cargarResumenProductos();
  await cargarProductosGrafica();
})();
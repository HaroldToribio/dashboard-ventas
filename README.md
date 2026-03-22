# 📊 Sistema de Control de Inventario Inteligente

Aplicación fullstack de gestión y predicción de inventario con Machine Learning.  
Incluye dashboard interactivo, modelos de regresión para predecir demanda, gestión de productos y reportes gráficos — todo conectado a una base de datos MySQL mediante una API REST en Flask.

---

## 🎬 Demo

https://github.com/user-attachments/assets/c93959e3-8cbb-47cb-b467-ffbeda71018d

---

## 🚀 Funcionalidades

- 🤖 **Predicción de demanda con ML** — compara 4 modelos de regresión automáticamente y selecciona el mejor
- 📊 **Comparación de modelos** — tabla con métricas MAE y R² para LinearRegression, DecisionTree, RandomForest y GradientBoosting
- 📈 **Dashboard interactivo** — KPIs en tiempo real: ventas totales, promedio, producto top
- 📦 **Gestión de productos** — crear, listar y eliminar productos
- 🧪 **Simulación de historial** — al agregar un producto, genera 90 días de ventas simuladas automáticamente para que el modelo ML pueda predecir desde el primer momento
- 📉 **Reportes gráficos** — ventas por producto en gráficas de barras y torta (Chart.js)
- 🔒 **Seguridad SQL** — todas las operaciones usan stored procedures, sin queries concatenadas

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3, Flask, Flask-CORS |
| Base de datos | MySQL 8 + Stored Procedures |
| Machine Learning | scikit-learn (LinearRegression, RandomForest, GradientBoosting, DecisionTree) |
| Encoders | LabelEncoder, OneHotEncoder, OrdinalEncoder |
| Frontend | HTML5, CSS3, JavaScript (Vanilla) |
| Gráficas | Chart.js |

---

## 📂 Estructura del proyecto

```
dashboard-ventas/
│
├── backend/
│   ├── api.py                        ← Endpoints Flask
│   ├── data_loader.py                ← Carga historial de MySQL a DataFrame
│   ├── encoders.py                   ← Encoders de clasificación
│   ├── database/
│   │   └── connection.py             ← Conexión MySQL (variables de entorno)
│   ├── repositories/
│   │   └── ventas_repository.py      ← Llamadas a stored procedures
│   └── services/
│       ├── modelo_ml.py              ← Entrenamiento y comparación de modelos
│       └── prediccion_service.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── dashboard.js
│
├── DB_Control_Inventario.sql         ← Schema + stored procedures + datos de prueba
├── .env.example                      ← Plantilla de variables de entorno
├── .gitignore
└── README.md
```

---

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/HaroldToribio/dashboard-ventas.git
cd dashboard-ventas
```

### 2. Crear y activar entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install flask flask-cors mysql-connector-python pandas scikit-learn numpy
```

### 4. Configurar la base de datos

Ejecutar el script SQL en MySQL Workbench o desde terminal:

```bash
mysql -u root -p < DB_Control_Inventario.sql
```

Esto crea la base de datos, las tablas, todos los stored procedures y los datos de prueba.

### 5. Configurar variables de entorno

Copia `.env.example` a `.env` y llena tus credenciales:

```bash
# Windows
set DB_HOST=localhost
set DB_USER=root
set DB_PASSWORD=tu_password
set DB_NAME=inventariosimulacion

# Mac / Linux
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=tu_password
export DB_NAME=inventariosimulacion
```

### 6. Ejecutar el backend

```bash
python -m flask --app backend.api run --debug
```

API disponible en: `http://127.0.0.1:5000`

### 7. Ejecutar el frontend

Abre `frontend/index.html` en el navegador, o usa un servidor local:

```bash
cd frontend && python -m http.server 8080
```

Luego visita: `http://localhost:8080`

---

## 📡 Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/productos` | Lista todos los productos |
| `POST` | `/productos` | Crea producto y genera historial simulado |
| `DELETE` | `/productos/<id>` | Elimina producto y sus ventas |
| `GET` | `/ventas` | Todas las ventas con detalle |
| `GET` | `/ventas/<id>` | Ventas de un producto específico |
| `GET` | `/ventas-por-producto` | Resumen agrupado por producto |
| `GET` | `/prediccion/<id>?dias=7` | Predicción ML + comparación de modelos |
| `GET` | `/dashboard?producto=1&dias=7` | KPIs generales |

### Ejemplo de respuesta — `/prediccion/<id>`

```json
{
  "modelo_seleccionado": "RandomForest",
  "comparacion_modelos": {
    "LinearRegression":  { "MAE": 1.42, "R2": 0.81 },
    "DecisionTree":      { "MAE": 1.87, "R2": 0.74 },
    "RandomForest":      { "MAE": 1.21, "R2": 0.89 },
    "GradientBoosting":  { "MAE": 1.33, "R2": 0.86 }
  },
  "predicciones": [
    { "fecha": "2025-04-01", "prediccion": 8.5 },
    { "fecha": "2025-04-02", "prediccion": 7.3 }
  ],
  "estadisticas_historicas": {
    "promedio_diario": 8.2,
    "total_vendido": 738,
    "dias_registrados": 90
  }
}
```

---

## 🧠 Modelos de Machine Learning

El sistema entrena y compara automáticamente 4 modelos con cada consulta de predicción:

| Modelo | Descripción |
|--------|-------------|
| `LinearRegression` | Regresión lineal clásica — base de comparación |
| `DecisionTreeRegressor` | Árbol de decisión — captura relaciones no lineales |
| `RandomForestRegressor` | Ensemble de 100 árboles — robusto ante overfitting |
| `GradientBoostingRegressor` | Boosting secuencial — alta precisión en datos tabulares |

Las features usadas son extraídas de la fecha: `dia`, `mes`, `dia_semana`, `trimestre`.  
El modelo con menor MAE se selecciona automáticamente.

---

## 👨‍💻 Autor

**Harold Toribio**  
Proyecto Final — Segundo Parcial, Programación con Inteligencia Artificial
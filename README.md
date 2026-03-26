# 📊 Sistema de Control de Inventario Inteligente

Aplicación fullstack de gestión y predicción de inventario con Machine Learning y recomendaciones personalizadas.  
Combina una base de datos MySQL, una API REST en Flask, modelos de regresión con scikit-learn y un dashboard interactivo que muestra estadísticas, predicciones de demanda y recomendaciones de productos al estilo Amazon.

---

## 🎬 Demo

https://github.com/user-attachments/assets/f84a6784-dbf3-48f1-aaac-4c14ad57658a

---

## 🚀 Funcionalidades

### 🤖 Machine Learning
- Entrena y compara automáticamente 4 modelos de regresión: **LinearRegression, DecisionTree, RandomForest y GradientBoosting**
- Selecciona el mejor modelo por MAE y R² en cada consulta
- Predice demanda futura para 7, 14 o 30 días
- Encoders aplicados al feature engineering: **LabelEncoder, OneHotEncoder, OrdinalEncoder**

### 🛍️ Recomendaciones personalizadas
- **Filtrado colaborativo** basado en similitud coseno (igual que Amazon, Shein, Temu)
- Recomienda productos según el historial de clientes con patrones de compra similares
- Muestra score de afinidad y razón de cada recomendación

### 📈 Reportes avanzados
- Ingresos totales por producto (barras horizontales)
- Participación en unidades vendidas (dona)
- Tendencia mensual de ventas (línea + barras)
- **Pares de productos comprados juntos** con frecuencia — la base visible del motor de recomendaciones

### 📦 Gestión de inventario
- Crear, listar y eliminar productos
- Al agregar un producto, genera **90 días de historial simulado** automáticamente para activar las predicciones ML desde el primer momento
- Gestión de clientes con compras iniciales simuladas para el cold-start del filtrado colaborativo

### 🔒 Seguridad
- Todas las operaciones de base de datos usan **stored procedures** — sin queries concatenadas, sin riesgo de inyección SQL
- Credenciales manejadas con **variables de entorno**, nunca en el código fuente

---

## 🛠️ Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3, Flask, Flask-CORS |
| Base de datos | MySQL 8 + Stored Procedures |
| Machine Learning | scikit-learn (LinearRegression, RandomForest, GradientBoosting, DecisionTree) |
| Encoders | LabelEncoder, OneHotEncoder, OrdinalEncoder |
| Recomendaciones | Filtrado colaborativo con similitud coseno (sklearn.metrics.pairwise) |
| Frontend | HTML5, CSS3, JavaScript Vanilla |
| Gráficas | Chart.js |

---

## 📂 Estructura del proyecto

```
dashboard-ventas/
│
├── backend/
│   ├── api.py                          ← Endpoints Flask
│   ├── data_loader.py                  ← Carga historial MySQL → DataFrame
│   ├── encoders.py                     ← LabelEncoder, OneHot, Ordinal
│   ├── database/
│   │   └── connection.py               ← Conexión MySQL (variables de entorno)
│   ├── repositories/
│   │   ├── ventas_repository.py        ← Stored procedures de ventas y productos
│   │   └── clientes_repository.py      ← Stored procedures de clientes
│   └── services/
│       ├── modelo_ml.py                ← Entrenamiento y comparación de modelos
│       ├── prediccion_service.py       ← Orquesta predicción ML
│       └── recomendacion_service.py    ← Filtrado colaborativo (similitud coseno)
│
├── frontend/
│   ├── index.html                      ← Dashboard, Productos, Predicción, Recomendaciones, Reportes
│   ├── style.css
│   └── dashboard.js
│
├── DB_Control_Inventario.sql           ← Schema + stored procedures + datos de prueba
├── .env.example                        ← Plantilla de variables de entorno
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
| `POST` | `/productos` | Crea producto + genera 90 días de historial simulado |
| `DELETE` | `/productos/<id>` | Elimina producto y sus ventas |
| `GET` | `/ventas` | Todas las ventas con detalle |
| `GET` | `/ventas-por-producto` | Resumen agrupado por producto |
| `GET` | `/prediccion/<id>?dias=7` | Predicción ML + comparación de 4 modelos |
| `GET` | `/clientes` | Lista todos los clientes |
| `POST` | `/clientes` | Crea cliente + simula compras iniciales |
| `GET` | `/recomendaciones/<id>?top=3` | Recomendaciones por filtrado colaborativo |
| `GET` | `/reportes/ventas-por-mes` | Tendencia mensual de ventas |
| `GET` | `/reportes/pares-productos` | Productos comprados juntos con más frecuencia |
| `GET` | `/dashboard?producto=1&dias=7` | KPIs generales |

### Ejemplo — `/prediccion/<id>`

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

### Ejemplo — `/recomendaciones/<id>`

```json
{
  "id_cliente": 3,
  "total_clientes_analizados": 8,
  "historial_compras": [
    { "id_producto": 1, "nombre": "Laptop", "cantidad": 5 }
  ],
  "recomendaciones": [
    {
      "id_producto": 2,
      "nombre": "Mouse",
      "precio": 25.50,
      "score": 0.87,
      "razon": "4 cliente(s) con perfil similar también lo compraron"
    }
  ]
}
```

---

## 🧠 Modelos de Machine Learning

| Modelo | Descripción |
|--------|-------------|
| `LinearRegression` | Regresión lineal — base de comparación |
| `DecisionTreeRegressor` | Árbol de decisión — relaciones no lineales simples |
| `RandomForestRegressor` | Ensemble de 100 árboles — robusto ante overfitting |
| `GradientBoostingRegressor` | Boosting secuencial — alta precisión en datos tabulares |

Features extraídas de la fecha: `dia`, `mes`, `dia_semana`, `trimestre`.  
El modelo con menor MAE se selecciona automáticamente.

---

## 👨‍💻 Autor

**Harold Toribio**  
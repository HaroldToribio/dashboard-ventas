# 📊 Dashboard de Ventas

Aplicación web desarrollada para la gestión y visualización de ventas en tiempo real.  
Incluye dashboard interactivo, gestión de productos y reportes gráficos.

---

## 🚀 Funcionalidades

- 📈 Visualización de ventas en gráfico (Chart.js)
- 📦 Gestión de productos (crear y listar)
- 📊 Reportes de ventas por producto
- 💰 Cálculo automático de:
  - Ventas totales
  - Promedio de ventas
- 📉 Resumen visual dinámico

---

## 🛠️ Tecnologías utilizadas

### Backend
- Python
- Flask
- MySQL

### Frontend
- HTML5
- CSS3
- JavaScript
- Chart.js

---

## 📂 Estructura del proyecto


dashboard-ventas/
│
├── backend/
│ ├── api.py
│ ├── repositories/
│ └── database/
│
├── frontend/
│ ├── index.html
│ ├── style.css
│ └── dashboard.js
│
├── .gitignore
└── README.md


---

## ⚙️ Instalación y ejecución

### 1. Clonar repositorio


git clone https://github.com/TU-USUARIO/dashboard-ventas.git

cd dashboard-ventas


---

### 2. Crear entorno virtual


python -m venv venv


Activar entorno:

- Windows:

venv\Scripts\activate


---

### 3. Instalar dependencias


pip install flask flask-cors mysql-connector-python


---

### 4. Configurar base de datos

- Crear base de datos en MySQL
- Crear tablas `productos` y `ventas`
- Configurar credenciales en:


backend/database/connection.py


---

### 5. Ejecutar backend


python backend/api.py


Servidor:

http://127.0.0.1:5000


---

### 6. Ejecutar frontend

Abrir:


frontend/index.html


(O usar Live Server)

---

## 📸 Capturas del sistema

> Aquí puedes agregar screenshots del dashboard, productos y reportes.

---

## 📌 Endpoints principales

- `GET /ventas`
- `GET /productos`
- `POST /productos`
- `GET /ventas-por-producto`

---

## 🎯 Objetivo del proyecto

Este proyecto fue desarrollado como práctica de integración fullstack, permitiendo consolidar conocimientos en:

- Desarrollo backend con Flask
- Consumo de APIs con JavaScript
- Visualización de datos
- Manejo de bases de datos relacionales

---

## 👨‍💻 Autor

**Harold Toribio**

---

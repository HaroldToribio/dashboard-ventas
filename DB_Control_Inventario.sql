-- =========================================
-- CREAR BASE DE DATOS
-- =========================================
CREATE DATABASE IF NOT EXISTS InventarioSimulacion;
USE InventarioSimulacion;

-- =========================================
-- TABLA PRODUCTOS
-- =========================================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    precio DECIMAL(10,2)
);

-- =========================================
-- TABLA VENTAS
-- =========================================
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_producto INT,
    fecha DATE,
    cantidad INT,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);

-- =========================================
-- INSERTAR DATOS DE PRUEBA
-- =========================================
INSERT INTO productos (nombre, categoria, precio) VALUES
('Laptop', 'Tecnologia', 1200.00),
('Mouse', 'Tecnologia', 25.50),
('Teclado', 'Tecnologia', 45.00);

INSERT INTO ventas (id_producto, fecha, cantidad) VALUES
(1, '2024-01-01', 5),
(1, '2024-01-05', 8),
(1, '2024-01-10', 6),
(2, '2024-01-02', 10),
(2, '2024-01-06', 15),
(3, '2024-01-03', 7);

-- =========================================
-- STORED PROCEDURE: OBTENER VENTAS POR PRODUCTO
-- =========================================
DELIMITER $$

CREATE PROCEDURE ObtenerVentasPorProducto(IN p_id_producto INT)
BEGIN
    SELECT 
        fecha,
        cantidad
    FROM ventas
    WHERE id_producto = p_id_producto
    ORDER BY fecha;
END$$

DELIMITER ;

-- =========================================
-- STORED PROCEDURE: LISTAR PRODUCTOS
-- =========================================
DELIMITER $$
 
CREATE PROCEDURE ListarProductos()
BEGIN
    SELECT id_producto, nombre, categoria, precio
    FROM productos
    ORDER BY nombre;
END$$
 
DELIMITER ;

-- =========================================
-- STORED PROCEDURE: INSERTAR VENTA
-- =========================================

DELIMITER $$

CREATE PROCEDURE InsertarVenta(
    IN p_id_producto INT,
    IN p_fecha DATE,
    IN p_cantidad INT
)
BEGIN
    INSERT INTO ventas (id_producto, fecha, cantidad)
    VALUES (p_id_producto, p_fecha, p_cantidad);
END$$

DELIMITER ;

-- =========================================
-- PRUEBAS
-- =========================================

-- Ver productos
CALL ListarProductos();

-- Ver ventas de un producto
CALL ObtenerVentasPorProducto(1);

-- Insertar nueva venta
CALL InsertarVenta(1, '2024-01-15', 12);

-- Ver todas las ventas
CALL ObtenerVentasTotales();

-- =========================================
-- SP: VENTAS TOTALES (todas las filas con fecha)
-- =========================================
DELIMITER $$
 
CREATE PROCEDURE ObtenerVentasTotales()
BEGIN
    SELECT
        v.id_venta,
        p.nombre,
        v.fecha,
        v.cantidad,
        ROUND(v.cantidad * p.precio, 2) AS total
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
    ORDER BY v.fecha DESC;
END$$
 
DELIMITER ;

-- =========================================
-- SP: CREAR PRODUCTO
-- =========================================

DELIMITER $$

CREATE PROCEDURE CrearProducto(
    IN p_nombre VARCHAR(100),
    IN p_precio DECIMAL(10,2)
)
BEGIN
    INSERT INTO productos (nombre, categoria, precio)
    VALUES (p_nombre, 'General', p_precio);
END$$

DELIMITER ;

-- =========================================
-- SP: ELIMINAR PRODUCTO
-- =========================================
DELIMITER $$
 
CREATE PROCEDURE EliminarProducto(IN p_id INT)
BEGIN
    DELETE FROM ventas    WHERE id_producto = p_id;
    DELETE FROM productos WHERE id_producto = p_id;
END$$
 
DELIMITER ;

DELIMITER $$

-- =========================================
-- SP: RESUMEN DE VENTAS (agrupado por producto)
-- =========================================
DELIMITER $$
 
CREATE PROCEDURE ObtenerResumenVentas()
BEGIN
    SELECT
        p.id_producto,
        p.nombre,
        SUM(v.cantidad * p.precio) AS total,
        SUM(v.cantidad)            AS unidades
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto
    GROUP BY p.id_producto, p.nombre
    ORDER BY total DESC;
END$$
 
DELIMITER ;

-- =========================================
-- SP: DASHBOARD RESUMEN GENERAL
-- =========================================

DELIMITER $$
 
CREATE PROCEDURE ObtenerDashboardResumen()
BEGIN
    SELECT
        COUNT(DISTINCT v.id_venta)           AS total_registros,
        ROUND(SUM(v.cantidad * p.precio), 2) AS total_ventas,
        ROUND(AVG(v.cantidad * p.precio), 2) AS promedio_ventas,
        COUNT(DISTINCT p.id_producto)        AS total_productos,
        (
            SELECT p2.nombre
            FROM ventas v2
            JOIN productos p2 ON v2.id_producto = p2.id_producto
            GROUP BY p2.id_producto
            ORDER BY SUM(v2.cantidad) DESC
            LIMIT 1
        ) AS producto_top
    FROM ventas v
    JOIN productos p ON v.id_producto = p.id_producto;
END$$
 
DELIMITER ;

-- =========================================
-- VERIFICACION
-- =========================================
CALL ListarProductos();
CALL ObtenerResumenVentas();
CALL ObtenerDashboardResumen();

-- =========================================
-- SP: SIMULAR VENTAS HISTÓRICAS
-- Genera ~90 días de ventas simuladas para un producto nuevo.
-- p_promedio: promedio diario estimado por el usuario
-- La cantidad por día varía ±50% del promedio (distribución uniforme)
-- para simular fluctuación real de ventas.
-- =========================================
DELIMITER $$
 
CREATE PROCEDURE SimularVentasHistoricas(
    IN p_id_producto INT,
    IN p_promedio    INT,
    IN p_dias        INT   -- normalmente 90
)
BEGIN
    DECLARE i       INT DEFAULT 0;
    DECLARE cantidad INT;
    DECLARE fecha_venta DATE;
    DECLARE minimo  INT;
    DECLARE maximo  INT;
 
    SET minimo = GREATEST(1, ROUND(p_promedio * 0.5));
    SET maximo = ROUND(p_promedio * 1.5);
 
    WHILE i < p_dias DO
        SET fecha_venta = DATE_SUB(CURDATE(), INTERVAL (p_dias - i) DAY);
        -- Cantidad aleatoria entre minimo y maximo
        SET cantidad = minimo + FLOOR(RAND() * (maximo - minimo + 1));
 
        INSERT INTO ventas (id_producto, fecha, cantidad)
        VALUES (p_id_producto, fecha_venta, cantidad);
 
        SET i = i + 1;
    END WHILE;
END$$
 
DELIMITER ;
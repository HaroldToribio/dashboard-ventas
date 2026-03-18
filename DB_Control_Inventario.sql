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
    SELECT * FROM productos;
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

DESCRIBE productos;

SELECT 
    v.fecha,
    (v.cantidad * p.precio) AS total
FROM ventas v
JOIN productos p ON v.id_producto = p.id_producto;
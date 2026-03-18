from backend.database.connection import DatabaseConnection
from flask import jsonify, request, Response
from typing import Union, Tuple

class VentasRepository:

    def get_productos(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
                       SELECT id_producto AS id, nombre, precio
                       FROM productos
                       """)
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    def crear_producto(self, nombre, precio):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO productos (nombre, categoria, precio) VALUES (%s, %s, %s)",
            (nombre, "General", precio)
        )

        conn.commit()
        conn.close()

    def eliminar_producto(self, id):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM productos WHERE id_producto = %s"
        cursor.execute(query, (id,))
        conn.commit()

        cursor.close()
        conn.close()

    def get_dashboard(self, producto, dias):
        return {
            "prediccion": [10, 12, 15, 20, 18, 25, 30],
            "costo_total": 500,
            "inventario_final": 120,
            "demanda_promedio": 18
        }
    
    def obtener_resumen_ventas(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                p.nombre,
                SUM(v.cantidad * p.precio) AS total
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            GROUP BY p.nombre
        """)

        data = cursor.fetchall()
        conn.close()
        return data
    
    def obtener_ventas_por_producto(self, id_producto):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                v.fecha,
                (v.cantidad * p.precio) AS total
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            WHERE v.id_producto = %s
            ORDER BY v.fecha
        """, (id_producto,))

        data = cursor.fetchall()
        conn.close()
        return data
    
    def obtener_ventas(self):
        conn = DatabaseConnection().get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                v.fecha,
                (v.cantidad * p.precio) AS total
            FROM ventas v
            JOIN productos p ON v.id_producto = p.id_producto
            ORDER BY v.fecha
        """)

        data = cursor.fetchall()
        conn.close()
        return data
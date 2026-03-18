class Producto:
    def __init__(self, id_producto: int, nombre: str, categoria: str, precio: float):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    def to_dict(self):
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": float(self.precio)  # evita problemas con Decimal
        }

    def __repr__(self):
        return f"Producto({self.id_producto}, {self.nombre})"
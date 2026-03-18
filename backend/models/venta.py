class Venta:
    def __init__(self, fecha, cantidad):
        self.fecha = fecha
        self.cantidad = cantidad

    def to_dict(self):
        return {
            "fecha": self.fecha.strftime("%Y-%m-%d") if hasattr(self.fecha, "strftime") else self.fecha,
            "cantidad": self.cantidad
        }

    def __repr__(self):
        return f"Venta({self.fecha}, {self.cantidad})"
import pandas as pd
from backend.repositories.ventas_repository import VentasRepository

def cargar_datos(producto_id):
    repo = VentasRepository()
    ventas = repo.obtener_ventas_por_producto(producto_id)

    data = []

    for v in ventas:
        data.append({
            "fecha": v.fecha,
            "demanda": v.cantidad
        })

    df = pd.DataFrame(data)

    if not df.empty:
        df["fecha"] = pd.to_datetime(df["fecha"])

    return df
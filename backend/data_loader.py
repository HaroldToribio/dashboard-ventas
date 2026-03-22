import pandas as pd
from backend.repositories.ventas_repository import VentasRepository

def cargar_datos(producto_id):
    repo = VentasRepository()
    ventas = repo.obtener_ventas_por_producto(producto_id)

    data = []

    for v in ventas:
        # v es un dict (cursor dictionary=True), no un objeto
        data.append({
            "fecha": v["fecha"], # type: ignore
            "demanda": v["cantidad"] # type: ignore
        })

    df = pd.DataFrame(data)

    if not df.empty:
        df["fecha"] = pd.to_datetime(df["fecha"])

    return df
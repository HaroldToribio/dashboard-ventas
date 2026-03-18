import numpy as np

def calcular_estadisticas(df):

    return {
        "demanda_promedio": float(df["demanda"].mean()),
        "demanda_max": int(df["demanda"].max()),
        "demanda_min": int(df["demanda"].min()),
        "total_registros": int(len(df))
    }
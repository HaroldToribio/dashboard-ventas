import numpy as np

from montecarlo import generar_demanda
from inventario_simulador import simular_inventario

def ejecutar_simulacion(predicciones):

    escenarios = generar_demanda(predicciones)

    resultados = []

    for demanda in escenarios:

        costo = simular_inventario(demanda, s=20, S=120)

        resultados.append(costo)

    return {
        "costo_promedio": np.mean(resultados),
        "costo_min": np.min(resultados),
        "costo_max": np.max(resultados)
    }
import numpy as np

from montecarlo import generar_demanda
from inventario_simulador import simular_inventario

def optimizar_parametros(predicciones):

    escenarios = generar_demanda(predicciones)

    mejor_costo = float("inf")
    mejor_s = None
    mejor_S = None

    for s in range(10,50,5):

        for S in range(80,200,10):

            costos = []

            for demanda in escenarios:

                costo = simular_inventario(demanda,s,S)

                costos.append(costo)

            costo_promedio = np.mean(costos)

            if costo_promedio < mejor_costo:

                mejor_costo = costo_promedio

                mejor_s = s

                mejor_S = S

    return {
        "mejor_s": int(mejor_s),
        "mejor_S": int(mejor_S),
        "costo_minimo": float(mejor_costo)
    }
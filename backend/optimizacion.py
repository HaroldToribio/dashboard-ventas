import numpy as np
from simulacion import simular_inventario


def optimizar_politica(predicciones):

    mejor_s = None
    mejor_S = None
    costo_minimo = float("inf")

    for s in range(5, 30, 5):
        for S in range(40, 120, 10):

            costos = []

            for _ in range(30):

                resultado = simular_inventario(
                    predicciones,
                    s=s,
                    S=S
                )

                costos.append(resultado["costo_total"])

            costo_promedio = np.mean(costos)

            if costo_promedio < costo_minimo:
                costo_minimo = costo_promedio
                mejor_s = s
                mejor_S = S

    return {
        "mejor_s": int(mejor_s),
        "mejor_S": int(mejor_S),
        "costo_minimo": float(costo_minimo)
    }
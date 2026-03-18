import numpy as np

def generar_demanda(predicciones, simulaciones=1000):

    media = np.mean(predicciones)
    desviacion = np.std(predicciones)

    demandas = []

    for _ in range(simulaciones):

        escenario = np.random.normal(
            media,
            desviacion,
            len(predicciones)
        )

        escenario = np.maximum(0, escenario)

        demandas.append(escenario)

    return demandas
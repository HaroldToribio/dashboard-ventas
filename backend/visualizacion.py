import matplotlib.pyplot as plt
import seaborn as sns

def grafico_demanda(df):

    plt.figure()

    sns.histplot(df["cantidad"], bins=20, kde=True)

    plt.title("Distribución de Demanda")

    plt.xlabel("Cantidad vendida")

    plt.ylabel("Frecuencia")

    plt.show()

def grafico_modelos(resultados):

    modelos = list(resultados.keys())

    mae = [resultados[m]["MAE"] for m in modelos]

    plt.figure()

    plt.bar(modelos, mae)

    plt.title("Comparación de Modelos ML")

    plt.ylabel("MAE (Error Medio Absoluto)")

    plt.show()

def grafico_montecarlo(escenarios):

    import numpy as np

    todas = np.concatenate(escenarios)

    plt.figure()

    sns.histplot(todas, bins=30)

    plt.title("Distribución Demanda Simulada (Monte Carlo)")

    plt.xlabel("Demanda")

    plt.ylabel("Frecuencia")

    plt.show()

def grafico_costos(costos):

    plt.figure()

    sns.histplot(costos, bins=30)

    plt.title("Distribución de Costos de Inventario")

    plt.xlabel("Costo total")

    plt.ylabel("Frecuencia")

    plt.show()
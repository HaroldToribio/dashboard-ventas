import pandas as pd
from sklearn.ensemble import RandomForestRegressor


def crear_features(df):

    df = df.copy()

    df["dia"] = df["fecha"].dt.day
    df["mes"] = df["fecha"].dt.month
    df["dia_semana"] = df["fecha"].dt.weekday

    return df


def entrenar_modelo(df):

    df = crear_features(df)

    X = df[["dia", "mes", "dia_semana"]]
    y = df["demanda"]

    modelo = RandomForestRegressor()

    modelo.fit(X, y)

    return modelo


def predecir_demanda(modelo):

    fechas_futuras = pd.date_range(start="2025-01-01", periods=7)

    df_pred = pd.DataFrame({"fecha": fechas_futuras})

    df_pred = crear_features(df_pred)

    X_pred = df_pred[["dia", "mes", "dia_semana"]]

    predicciones = modelo.predict(X_pred)

    return predicciones.tolist()
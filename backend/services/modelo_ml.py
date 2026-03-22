import pandas as pd
import numpy as np
from datetime import timedelta

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import LabelEncoder


def crear_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["dia"]       = df["fecha"].dt.day
    df["mes"]       = df["fecha"].dt.month
    df["dia_semana"] = df["fecha"].dt.weekday          # 0=Lunes … 6=Domingo
    df["trimestre"] = df["fecha"].dt.quarter
    return df


# ─────────────────────────────────────────
# COMPARAR MODELOS Y SELECCIONAR EL MEJOR
# ─────────────────────────────────────────

def comparar_modelos(df: pd.DataFrame) -> dict:
    df = crear_features(df)

    if len(df) < 4:
        X = df[["dia", "mes", "dia_semana", "trimestre"]]
        y = df["demanda"]
        modelo = LinearRegression()
        modelo.fit(X, y)
        return {
            "mejor_modelo": modelo,
            "nombre_mejor": "LinearRegression",
            "resultados": {
                "LinearRegression": {"MAE": None, "R2": None}
            }
        }

    X = df[["dia", "mes", "dia_semana", "trimestre"]]
    y = df["demanda"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    candidatos = {
        "LinearRegression":   LinearRegression(),
        "DecisionTree":       DecisionTreeRegressor(random_state=42),
        "RandomForest":       RandomForestRegressor(n_estimators=100, random_state=42),
        "GradientBoosting":   GradientBoostingRegressor(n_estimators=100, random_state=42),
    }

    resultados = {}
    mejor_modelo  = None
    nombre_mejor  = None
    mejor_mae     = float("inf")

    for nombre, modelo in candidatos.items():
        modelo.fit(X_train, y_train)
        pred = modelo.predict(X_test)

        mae = float(mean_absolute_error(y_test, pred))
        r2  = float(r2_score(y_test, pred))

        resultados[nombre] = {"MAE": round(mae, 4), "R2": round(r2, 4)}

        if mae < mejor_mae:
            mejor_mae    = mae
            mejor_modelo = modelo
            nombre_mejor = nombre

    return {
        "mejor_modelo": mejor_modelo,
        "nombre_mejor": nombre_mejor,
        "resultados":   resultados
    }


# ─────────────────────────────────────────
# ENTRENAR (interfaz simple para prediccion_service)
# ─────────────────────────────────────────

def entrenar_modelo(df: pd.DataFrame):
    return comparar_modelos(df)["mejor_modelo"]


# ─────────────────────────────────────────
# PREDECIR DEMANDA FUTURA
# ─────────────────────────────────────────

def predecir_demanda(modelo, dias: int = 7) -> list:
    desde = pd.Timestamp.today().normalize() + timedelta(days=1)
    fechas_futuras = pd.date_range(start=desde, periods=dias)

    df_pred = pd.DataFrame({"fecha": fechas_futuras})
    df_pred = crear_features(df_pred)

    X_pred = df_pred[["dia", "mes", "dia_semana", "trimestre"]]
    predicciones = modelo.predict(X_pred)

    return [
        {
            "fecha": str(fecha.date()),
            "prediccion": round(float(pred), 2)
        }
        for fecha, pred in zip(fechas_futuras, predicciones)
    ]


# ─────────────────────────────────────────
# FUNCIÓN COMPLETA PARA EL ENDPOINT
# ─────────────────────────────────────────

def analizar_y_predecir(df: pd.DataFrame, dias: int = 7) -> dict:
    if df.empty:
        return {"error": "No hay datos históricos para este producto."}

    comparacion = comparar_modelos(df)
    mejor_modelo = comparacion["mejor_modelo"]

    predicciones = predecir_demanda(mejor_modelo, dias=dias)

    estadisticas = {
        "promedio_diario": round(float(df["demanda"].mean()), 2),
        "max_diario":      int(df["demanda"].max()),
        "min_diario":      int(df["demanda"].min()),
        "total_vendido":   int(df["demanda"].sum()),
        "dias_registrados": len(df)
    }

    return {
        "modelo_seleccionado": comparacion["nombre_mejor"],
        "comparacion_modelos": comparacion["resultados"],
        "predicciones":        predicciones,
        "estadisticas_historicas": estadisticas
    }
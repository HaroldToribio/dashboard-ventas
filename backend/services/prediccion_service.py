from backend.services.modelo_ml import analizar_y_predecir

def predecir_demanda(df, dias: int = 7) -> dict:
    return analizar_y_predecir(df, dias=dias)
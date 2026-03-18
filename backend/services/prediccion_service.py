from backend.services.modelo_ml import entrenar_modelo, predecir_demanda as predecir_modelo

def predecir_demanda(df):
    modelo = entrenar_modelo(df)
    return predecir_modelo(modelo)
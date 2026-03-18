from backend.data_loader import cargar_datos
from backend.dataset_builder import preparar_dataset
from backend.modelos import entrenar_modelos
from backend.services.prediccion_service import predecir_demanda
from backend.visualizacion import grafico_demanda
from backend.optimizador_inventario import optimizar_parametros

df = cargar_datos(1)

grafico_demanda(df)

X,y = preparar_dataset(df)

modelo = entrenar_modelos(X,y)

predicciones = predecir_demanda(modelo)

resultado = optimizar_parametros(predicciones)

print("Resultado optimización")

print(resultado)
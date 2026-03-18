from data_loader import cargar_datos
from dataset_builder import preparar_dataset
from modelos import entrenar_modelos

df = cargar_datos()

X,y = preparar_dataset(df)

resultados = entrenar_modelos(X,y)

print("Comparación de modelos")

for modelo,metricas in resultados.items():

    print(modelo)

    print("MAE:",metricas["MAE"])

    print("R2:",metricas["R2"])

    print("--------------")
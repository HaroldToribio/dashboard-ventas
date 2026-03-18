from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import GradientBoostingRegressor

def entrenar_modelos(X,y):

    X_train,X_test,y_train,y_test = train_test_split(
        X,y,test_size=0.2,random_state=42
    )

    modelos = {

        "LinearRegression": LinearRegression(),
        "DecisionTree": DecisionTreeRegressor(),
        "RandomForest": RandomForestRegressor(),
        "GradientBoosting": GradientBoostingRegressor()

    }

    resultados = {}

    mejor_modelo = None
    mejor_error = float("inf")

    for nombre,modelo in modelos.items():

        modelo.fit(X_train,y_train)

        pred = modelo.predict(X_test)

        mae = mean_absolute_error(y_test,pred)

        r2 = r2_score(y_test,pred)

        resultados[nombre] = {
            "MAE":mae,
            "R2":r2
        }

        print("Modelo:",nombre)
        print("MAE:",mae)
        print("R2:",r2)
        print("-----------")

        if mae < mejor_error:

            mejor_error = mae
            mejor_modelo = modelo

    print("Mejor modelo seleccionado")

    return mejor_modelo
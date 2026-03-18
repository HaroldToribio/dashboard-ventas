def preparar_dataset(df):

    df["dia_semana"] = df["fecha"].dt.dayofweek
    df["mes"] = df["fecha"].dt.month
    df["dia_mes"] = df["fecha"].dt.day

    X = df[["dia_semana","mes","dia_mes"]]
    y = df["cantidad"]

    return X, y
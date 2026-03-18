from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import OrdinalEncoder

def aplicar_label_encoder(df):

    le = LabelEncoder()

    df["dia_semana_enc"] = le.fit_transform(df["dia_semana"])

    return df


def aplicar_onehot_encoder(df):

    encoder = OneHotEncoder(sparse_output=False)

    encoded = encoder.fit_transform(df[["mes"]])

    return encoded


def aplicar_ordinal_encoder(df):

    encoder = OrdinalEncoder()

    df["mes_enc"] = encoder.fit_transform(df[["mes"]])

    return df
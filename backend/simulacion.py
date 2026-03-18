def simular_inventario(predicciones, s=10, S=80):

    inventario = S
    costo_total = 0
    faltantes = 0

    for demanda in predicciones:

        if inventario < demanda:
            faltantes += 1
            costo_total += 50

        inventario -= demanda

        if inventario <= s:
            pedido = S - inventario
            inventario += pedido
            costo_total += 100

    return {
        "inventario_final": inventario,
        "faltantes": faltantes,
        "costo_total": costo_total
    }
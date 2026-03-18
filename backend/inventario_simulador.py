def simular_inventario(demanda, s, S):

    inventario = S
    ventas_perdidas = 0
    pedidos = 0

    costo_almacenamiento = 1
    costo_faltante = 5
    costo_pedido = 50

    costo_total = 0

    for d in demanda:

        d = int(d)

        if inventario >= d:

            inventario -= d

        else:

            ventas_perdidas += d - inventario

            inventario = 0

        if inventario <= s:

            inventario = S

            pedidos += 1

            costo_total += costo_pedido

        costo_total += inventario * costo_almacenamiento

    costo_total += ventas_perdidas * costo_faltante

    return costo_total
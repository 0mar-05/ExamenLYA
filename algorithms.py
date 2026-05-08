from arbol import Nodo


def buscar_solucion_BFS(estado_inicial, solucion):
    solucionado = False
    nodos_visitados = []
    nodos_frontera = []
    nodo_inicial = Nodo(estado_inicial)
    nodos_frontera.append(nodo_inicial)

    while not solucionado and len(nodos_frontera) != 0:
        nodo = nodos_frontera.pop(0)
        nodos_visitados.append(nodo)

        if nodo.get_datos() == solucion:
            return nodo

        dato_nodo = nodo.get_datos()

        hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izquierdo = Nodo(hijo)
        if not hijo_izquierdo.en_lista(nodos_visitados) and not hijo_izquierdo.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_izquierdo)

        hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_central = Nodo(hijo)
        if not hijo_central.en_lista(nodos_visitados) and not hijo_central.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_central)

        hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_derecho = Nodo(hijo)
        if not hijo_derecho.en_lista(nodos_visitados) and not hijo_derecho.en_lista(nodos_frontera):
            nodos_frontera.append(hijo_derecho)

        nodo.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

    return None


def buscar_solucion_DFS_rec(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial

    dato_nodo = nodo_inicial.get_datos()

    hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
    hijo_izquierdo = Nodo(hijo)
    hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
    hijo_central = Nodo(hijo)
    hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
    hijo_derecho = Nodo(hijo)

    nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados:
            sol = buscar_solucion_DFS_rec(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol

    return None


def mejora(nodo_padre, nodo_hijo):
    calidad_padre = 0
    calidad_hijo = 0
    dato_padre = nodo_padre.get_datos()
    dato_hijo = nodo_hijo.get_datos()
    for n in range(1, len(dato_padre)):
        if dato_padre[n] > dato_padre[n - 1]:
            calidad_padre += 1
        if dato_hijo[n] > dato_hijo[n - 1]:
            calidad_hijo += 1
    return calidad_hijo >= calidad_padre


def buscar_solucion_heuristica(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial

    dato_nodo = nodo_inicial.get_datos()

    hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
    hijo_izquierdo = Nodo(hijo)

    hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
    hijo_central = Nodo(hijo)

    hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
    hijo_derecho = Nodo(hijo)

    nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

    for nodo_hijo in nodo_inicial.get_hijos():
        if nodo_hijo.get_datos() not in visitados and mejora(nodo_inicial, nodo_hijo):
            sol = buscar_solucion_heuristica(nodo_hijo, solucion, visitados)
            if sol is not None:
                return sol

    return None

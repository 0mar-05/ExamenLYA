# Puzzle Lineal con Heurística
from arbol import Nodo

# Bug 2 fix: mejora() definida a nivel de módulo, no anidada
def mejora(nodo_padre, nodo_hijo):
    calidad_padre = 0
    calidad_hijo = 0
    dato_padre = nodo_padre.get_datos()
    dato_hijo = nodo_hijo.get_datos()
    for n in range(1, len(dato_padre)):
        if dato_padre[n] > dato_padre[n-1]:   # Bug 3 fix: [] no ()
            calidad_padre += 1
        if dato_hijo[n] > dato_hijo[n-1]:     # Bug 3 fix: [] no ()
            calidad_hijo += 1
    return calidad_hijo >= calidad_padre


def buscar_solucion_heuristica(nodo_inicial, solucion, visitados):
    visitados.append(nodo_inicial.get_datos())
    if nodo_inicial.get_datos() == solucion:
        return nodo_inicial
    else:
        dato_nodo = nodo_inicial.get_datos()

        # Hijo Izquierdo
        hijo = [dato_nodo[1], dato_nodo[0], dato_nodo[2], dato_nodo[3]]
        hijo_izquierdo = Nodo(hijo)

        # Hijo Central — Bug 4 fix: dato_nodo[3] sin corchetes extra
        hijo = [dato_nodo[0], dato_nodo[2], dato_nodo[1], dato_nodo[3]]
        hijo_central = Nodo(hijo)

        # Hijo Derecho
        hijo = [dato_nodo[0], dato_nodo[1], dato_nodo[3], dato_nodo[2]]
        hijo_derecho = Nodo(hijo)

        nodo_inicial.set_hijos([hijo_izquierdo, hijo_central, hijo_derecho])

        for nodo_hijo in nodo_inicial.get_hijos():
            if nodo_hijo.get_datos() not in visitados and \
               mejora(nodo_inicial, nodo_hijo):
                sol = buscar_solucion_heuristica(nodo_hijo, solucion, visitados)
                if sol is not None:
                    return sol

        return None  # Bug 1 fix: fuera del for, no dentro


if __name__ == "__main__":
    estado_inicial = [4, 2, 3, 1]
    solucion = [1, 2, 3, 4]
    visitados = []
    nodo_inicial = Nodo(estado_inicial)

    nodo = buscar_solucion_heuristica(nodo_inicial, solucion, visitados)

    # Bug 5 fix: estas líneas fuera del while
    resultado = []
    while nodo.get_padre() is not None:
        resultado.append(nodo.get_datos())
        nodo = nodo.get_padre()

    resultado.append(estado_inicial)
    resultado.reverse()
    print(resultado)
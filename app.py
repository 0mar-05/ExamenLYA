from flask import Flask, render_template, request, jsonify
from algorithms import buscar_solucion_BFS, buscar_solucion_DFS_rec, buscar_solucion_heuristica
from arbol import Nodo

app = Flask(__name__, static_folder="static", template_folder="templates")

ALGORITHM_NAMES = {
    "bfs": "Búsqueda en Amplitud",
    "dfs": "Búsqueda en Profundidad",
    "heuristica": "Puzzle Lineal con Heurística",
}


def validate_state(state):
    if not isinstance(state, list) or len(state) != 4:
        return False
    if any(not isinstance(x, int) for x in state):
        return False
    return sorted(state) == [1, 2, 3, 4]


def build_path(nodo):
    path = []
    while nodo is not None:
        path.append(nodo.get_datos())
        nodo = nodo.get_padre()
    path.reverse()
    return path


@app.route("/")
def index():
    return render_template("index.html", algorithms=ALGORITHM_NAMES)


@app.route("/api/solve-all", methods=["POST"])
def solve_all():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido."}), 400

    initial = data.get("initial")
    goal = data.get("goal")

    if not validate_state(initial) or not validate_state(goal):
        return jsonify({"error": "Los estados deben ser listas de 4 números únicos del 1 al 4."}), 400

    try:
        bfs_node = buscar_solucion_BFS(initial, goal)
        dfs_node = buscar_solucion_DFS_rec(Nodo(initial), goal, [])
        heuristica_node = buscar_solucion_heuristica(Nodo(initial), goal, [])
    except Exception as exc:
        return jsonify({"error": f"Error interno al ejecutar los algoritmos: {exc}"}), 500

    if bfs_node is None or dfs_node is None or heuristica_node is None:
        return jsonify({"error": "No se encontró solución con uno o más algoritmos."}), 404

    results = []
    for key, nodo in [("bfs", bfs_node), ("dfs", dfs_node), ("heuristica", heuristica_node)]:
        results.append({
            "algorithm": ALGORITHM_NAMES[key],
            "steps": build_path(nodo),
            "length": len(build_path(nodo)) - 1,
        })

    return jsonify({"initial": initial, "goal": goal, "results": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

# Puzzle Lineal Web API

API y front-end para ejecutar los algoritmos `BFS`, `DFS` y `Puzzle Lineal con Heurística`.

## Instalación

1. Crear y activar el entorno virtual (opcional):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Ejecutar

```bash
python app.py
```

Abrir `http://localhost:5000` en el navegador.

## Despliegue

Para producción puedes usar `gunicorn`:

```bash
pip install gunicorn
gunicorn -b 0.0.0.0:5000 app:app
```

## Uso

- Selecciona el algoritmo.
- Completa los 4 números del estado inicial y los 4 números del estado objetivo.
- El front-end evitará seleccionar números duplicados en cada estado.
- Envía el formulario y verás la solución paso a paso.
# ExamenLYA
# ExamenLYA

# deitta-flattening-logic

Repositorio que contiene la lógica de aplanado de datos para Deitta.

## ¿Qué hace?

1. Lee transacciones no procesadas desde `data-process`.
2. Aplana los datos según su origen (`user_profile`, `form`, etc.).
3. Inserta registros en PostgreSQL (tablas `_current` y `_history`).
4. Confirma las transacciones procesadas.

## Estructura

- `app/main.py`: Punto de entrada de la Lambda.
- `app/flatteners/`: Lógica de aplanado por origen.
- `app/db/`: Conexión e inserción en DB.
- `tests/`: Pruebas unitarias.

## Configuración

Define las siguientes variables de entorno:
- `DATA_PROCESS_API_URL`
- `DATA_PROCESS_API_KEY`
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

Ejemplo de ejecución local:
```bash
export DATA_PROCESS_API_URL="https://api.dev/data-proccess/data-transactions"
export DATA_PROCESS_API_KEY="mi-api-key"
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="deitta_flattened"
export DB_USER="postgres"
export DB_PASSWORD="mysecretpass"

pytest

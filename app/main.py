import os
import json
from app.config import settings
from app.clients.data_process_client import DataProcessClient
from app.db.insert_handler import InsertHandler
from app.flatteners import base, user_profile, form, question_answer
from app.utils.logger import get_logger

logger = get_logger(__name__)

def handler(event, context):
    """
    Lambda handler invoked by AWS.

    1. Llama al microservicio data-process para obtener transacciones.
    2. Determina el dataOrigin y llama a la lógica de flatten correspondiente.
    3. Inserta en PostgreSQL.
    4. Confirma transacciones procesadas.
    """

    logger.info("Lambda execution started. Reading transactions...")

    # 1. Crear cliente y leer transacciones (no procesadas)
    client = DataProcessClient(settings.DATA_PROCESS_API_KEY, settings.DATA_PROCESS_API_URL)
    transactions = client.get_transactions(limit=100, processed=False)

    if not transactions:
        logger.info("No hay transacciones pendientes.")
        return {"message": "No new transactions to process."}

    # 2. Conectar a la BD
    insert_handler = InsertHandler(
        db_host=settings.DB_HOST,
        db_port=settings.DB_PORT,
        db_name=settings.DB_NAME,
        db_user=settings.DB_USER,
        db_password=settings.DB_PASSWORD
    )

    processed_ids = []

    for tx in transactions:
        data_origin = tx.get("dataOrigin")
        data_status = tx.get("dataStatus")
        data_content = tx.get("data", {})
        transaction_id = tx.get("transactionId")

        # 2.1 Seleccionar el flattener adecuado
        if data_origin == "user_profile":
            flattened_record = user_profile.flatten_user_profile(data_content, data_status)
        elif data_origin == "form":
            flattened_record = form.flatten_form(data_content, data_status)
        elif data_origin == "question_answer":
            flattened_record = question_answer.flatten_question_answer(data_content, data_status)
        else:
            # Si no reconocemos el data_origin, podemos ignorarlo o registrar un error
            logger.warning(f"Origen de datos desconocido: {data_origin}")
            continue

        # 2.2 Insertar en Postgres
        # flattened_record contendrá la info necesaria (category, subcategory, etc.)
        category = flattened_record.get("category", "default")
        insert_handler.insert_data(category, flattened_record)

        # Agregamos el transaction_id a la lista de procesados
        processed_ids.append(transaction_id)

    # 3. Confirmar transacciones procesadas
    if processed_ids:
        client.confirm_transactions(processed_ids)
        logger.info(f"Transacciones confirmadas: {processed_ids}")

    return {
        "message": f"Processed {len(processed_ids)} transactions",
        "processed_ids": processed_ids
    }

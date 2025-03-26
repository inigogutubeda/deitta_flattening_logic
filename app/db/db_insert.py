from .db_connection import DBConnection
import uuid
import datetime

class InsertHandler:
    def __init__(self, db_host, db_port, db_name, db_user, db_password):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password

    def insert_data(self, category, flattened_record):
        """
        Inserta el registro en la tabla {category}_current y, si aplica, {category}_history.
        """
        current_table = f"{category.lower()}_current"
        history_table = f"{category.lower()}_history"

        # Ejemplo: generamos un ID si no existe
        record_id = flattened_record.get("id", str(uuid.uuid4()))
        user_id = flattened_record.get("user_id")
        json_data = flattened_record.get("json", {})
        json_index = flattened_record.get("json_index", {})
        data_enrichment = flattened_record.get("data_enrichment", {})
        now = datetime.datetime.utcnow()

        with DBConnection(self.db_host, self.db_port, self.db_name, self.db_user, self.db_password) as conn:
            with conn.cursor() as cur:
                # Insert en la tabla *_current
                sql_current = f"""
                    INSERT INTO {current_table} (
                        id, user_id, json, json_index, data_enrichment, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE 
                    SET json = EXCLUDED.json,
                        json_index = EXCLUDED.json_index,
                        data_enrichment = EXCLUDED.data_enrichment,
                        updated_at = EXCLUDED.updated_at;
                """
                cur.execute(
                    sql_current,
                    (record_id, user_id, json_data, json_index, data_enrichment, now, now)
                )

                # Insert en la tabla *_history (si queremos trackear toda modificación)
                if flattened_record.get("save_history", True):
                    source_tx_id = flattened_record.get("source_transaction_id", str(uuid.uuid4()))
                    version_timestamp = now
                    sql_history = f"""
                        INSERT INTO {history_table} (
                            id, user_id, json, json_index, data_enrichment,
                            created_at, updated_at, version_timestamp, source_transaction_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cur.execute(
                        sql_history,
                        (
                            str(uuid.uuid4()), 
                            user_id, 
                            json_data, 
                            json_index, 
                            data_enrichment, 
                            now, 
                            now, 
                            version_timestamp, 
                            source_tx_id
                        )
                    )

        return record_id

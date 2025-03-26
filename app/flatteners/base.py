def base_flatten(data: dict, data_status: str) -> dict:
    """
    Función base genérica para aplanar. 
    Se puede sobreescribir en cada flattener específico.
    """
    return {
        "json": data,
        "json_index": {},  # construir índices según data
        "data_enrichment": {},
        "source_transaction_id": None,
        "save_history": True
    }

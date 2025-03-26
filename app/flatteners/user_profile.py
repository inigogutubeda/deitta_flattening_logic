from .base import base_flatten

def flatten_user_profile(data: dict, data_status: str) -> dict:
    """
    Aplana los datos de 'user_profile'.
    """
    result = base_flatten(data, data_status)
    result["category"] = "user_profile"

    # Ejemplo de índices para búsquedas
    # Supongamos que data = {"name": "Juan", "country": "España", ...}
    result["json_index"] = {
        "name": data.get("name"),
        "country": data.get("country")
    }

    # Ajusta la lógica según sea create/update/delete
    # (p.ej. si es delete, tal vez "save_history" = True con un estado 'deleted')

    return result

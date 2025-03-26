from .base import base_flatten

def flatten_form(data: dict, data_status: str) -> dict:
    """
    Aplana datos de origen form.
    """
    result = base_flatten(data, data_status)
    # Ej. data podría tener "category": "ocio", "subCategory": "streaming"
    form_cat = data.get("category", "default")
    result["category"] = form_cat.lower()  # p.ej. "ocio"

    # Indices
    result["json_index"] = {
        "form_name": data.get("form_name"),
        "category": data.get("category"),
        "sub_category": data.get("subCategory"),
    }
    return result

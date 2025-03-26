from .base import base_flatten

def flatten_question_answer(data: dict, data_status: str) -> dict:
    """
    Aplana datos de preguntas y respuestas (QsA).
    """
    result = base_flatten(data, data_status)
    # Ej. definimos "category" en base a algo del data
    qsa_cat = data.get("category", "default")
    result["category"] = qsa_cat.lower()
    result["json_index"] = {
        "questionnaire_name": data.get("name"),
        "num_questions": len(data.get("questions", []))
    }
    return result

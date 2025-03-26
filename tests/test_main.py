import pytest
from app.main import handler

def test_handler_no_transactions(monkeypatch):
    # Mockear la llamada a get_transactions para devolver vacío
    monkeypatch.setattr(
        "app.clients.data_process_client.DataProcessClient.get_transactions",
        lambda self, limit, processed: []
    )

    resp = handler({}, {})
    assert resp["message"] == "No new transactions to process."

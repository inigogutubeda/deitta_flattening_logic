import requests
import logging

class DataProcessClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    def get_transactions(self, limit=100, processed=False):
        url = f"{self.base_url}?limit={limit}&processed={str(processed).lower()}"
        headers = {"Api-Key": self.api_key}

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Suponemos que data["data"] contiene la lista de transacciones
            return data.get("data", [])
        else:
            logging.error(f"Error fetching transactions. Status: {response.status_code}")
            return []

    def confirm_transactions(self, transaction_ids):
        url = f"{self.base_url}/confirm"
        headers = {"Api-Key": self.api_key}
        payload = {"transactionIds": transaction_ids}

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            logging.info("Transacciones confirmadas con éxito.")
        else:
            logging.error(f"Error confirming transactions. Status: {response.status_code}")

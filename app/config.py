import os

class Settings:
    # Config del microservicio Data Process
    DATA_PROCESS_API_URL = os.getenv("DATA_PROCESS_API_URL", "https://api.dev/data-proccess/data-transactions")
    DATA_PROCESS_API_KEY = os.getenv("DATA_PROCESS_API_KEY", "example-api-key")

    # Config DB
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "deitta_flattened")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

settings = Settings()

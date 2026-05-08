import os

class Config:
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "1234")
    MYSQL_DB = os.environ.get("MYSQL_DB", "rancho")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3309))
    SECRET_KEY = os.environ.get("SECRET_KEY", "super_secret_key")

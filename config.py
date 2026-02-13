import os

class DevConfig:
    DATABASE_URL = (
        f"mysql+pymysql://appuser:openPass0301@"
        f"@127.0.0.1:3306/appdb"
    )

class ProdConfig:
    DATABASE_URL = (
        "mysql+pymysql://appuser:"
        + os.environ["DB_PASSWORD"]
        + "@/appdb"
        + "?unix_socket=/cloudsql/platinum-linker-487308-t8:asia-northeast1:flask-mysql"
    )

def get_config():
    if os.environ.get("FLASK_ENV") == "development":
        return DevConfig
    return ProdConfig

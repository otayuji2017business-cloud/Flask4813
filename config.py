import os

class ProdConfig:
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD environment variable not set")

    DATABASE_URL = (
        f"mysql+pymysql://appuser:{DB_PASSWORD}"
        f"@/appdb"
        f"?unix_socket=/cloudsql/platinum-linker-487308-t8:asia-northeast1:flask-mysql"
    )

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from app.config import settings
import pandas as pd


def get_engine() -> Engine:
    conn_str = (
        f"postgresql://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    return create_engine(conn_str)


def read_sql(query: str, params=None) -> pd.DataFrame:
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn, params=params)

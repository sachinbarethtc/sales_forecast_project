# from sqlalchemy import create_engine, text
# from sqlalchemy.engine.url import URL
# from app.config import settings
# import pandas as pd

# def get_engine():
#     url = URL.create(
#         "postgresql+psycopg2",
#         username=settings.DB_USER,
#         password=settings.DB_PASSWORD,
#         host=settings.DB_HOST,
#         port=settings.DB_PORT,
#         database=settings.DB_NAME
#     )
#     engine = create_engine(url, pool_size=10, max_overflow=20)
#     return engine

# def read_sql(query: str, params: dict = None) -> pd.DataFrame:
#     engine = get_engine()
#     with engine.connect() as conn:
#         df = pd.read_sql_query(text(query), conn, params=params)
#     return df

# def execute_sql(sql: str, params: dict = None):
#     engine = get_engine()
#     with engine.begin() as conn:
#         conn.execute(text(sql), params or {})


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

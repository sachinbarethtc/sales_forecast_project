# # ingest.py
# from datetime import datetime
# import pandas as pd
# from app.db import read_sql
# from app.queries import DAY_AGG_SQL
# from app.logger import logger
# from app.config import settings


# def get_date_range_from_db():
#     q = f"""
#     SELECT 
#         MIN(bill_date)::date AS min_date,
#         MAX(bill_date)::date AS max_date
#     FROM {settings.TARGET_SCHEMA}.{settings.SOURCE_TABLE1};
#     """
#     df = read_sql(q)
#     return df["min_date"][0], df["max_date"][0]


# def fetch_day_aggregates(start_date=None, end_date=None):
#     db_min, db_max = get_date_range_from_db()

#     # Respect user-provided boundaries
#     if start_date is None:
#         start_date = db_min

#     if end_date is None:
#         end_date = db_max

#     logger.info(f"[INGEST] Fetching sales from {start_date}")

#     query = DAY_AGG_SQL.format(
#         schema=settings.TARGET_SCHEMA,
#         sales_table=settings.SOURCE_TABLE1,
#         assort_table=settings.SOURCE_TABLE2,
#     )

#     df = read_sql(query, {"start_date": start_date, "end_date": end_date})

#     if df.empty:
#         logger.warning("[INGEST] No data returned!")
#         return pd.DataFrame(columns=["day", "site_code", "assortment_name", "total_qty"])

#     df = df[df["total_qty"] >= 0]

#     out = df.groupby(["day", "site_code", "assortment_name"], as_index=False)["total_qty"].sum()
#     return out


from datetime import datetime, timedelta
import pandas as pd
from app.db import read_sql
from app.queries import DAY_AGG_SQL
from app.logger import logger
from app.config import settings


def get_date_range_from_db():
    q = f"""
    SELECT 
        MIN(bill_date)::date AS min_date,
        MAX(bill_date)::date AS max_date
    FROM {settings.TARGET_SCHEMA}.{settings.SOURCE_TABLE1};
    """
    df = read_sql(q)
    return df["min_date"][0], df["max_date"][0]


def fetch_day_aggregates(start_date=None, end_date=None):
    db_min, db_max = get_date_range_from_db()

    # Fetch ONLY last 365 days to prevent DB crash
    lookback_days = 365

    if start_date is None:
        start_date = max(db_min, db_max - timedelta(days=lookback_days))

    if end_date is None:
        end_date = db_max

    logger.info(f"[INGEST] Fetching sales from {start_date} to {end_date}")

    query = DAY_AGG_SQL.format(
        schema=settings.TARGET_SCHEMA,
        sales_table=settings.SOURCE_TABLE1,
        assort_table=settings.SOURCE_TABLE2,
    )

    df = read_sql(query, {"start_date": start_date, "end_date": end_date})

    if df.empty:
        logger.warning("[INGEST] No data returned!")
        return pd.DataFrame(columns=["day", "site_code", "assortment_name", "total_qty"])

    df = df[df["total_qty"] >= 0]

    out = df.groupby(["day", "site_code", "assortment_name"], as_index=False)["total_qty"].sum()
    return out

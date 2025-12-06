# # # # # from datetime import datetime
# # # # # from app.db import read_sql
# # # # # from app.queries import DAY_AGG_SQL
# # # # # from app.config import settings
# # # # # import pandas as pd

# # # # # def fetch_day_aggregates(start_date: str, end_date: str):
# # # # #     query = DAY_AGG_SQL.format(
# # # # #         schema=settings.source_schema,
# # # # #         sales_table=settings.generic_sales_history,   # generic_sales_history
# # # # #         assort_table=settings.generic_final_assortment   # generic_final_assortment
# # # # #     )
    
# # # # #     params = {"start_date": start_date, "end_date": end_date}
# # # # #     df = read_sql(query, params)

# # # # #     # Negative qty rows remove (your notebook logic)
# # # # #     df = df[df['total_qty'] >= 0]

# # # # #     # Daily aggregated total qty per assortment across all products
# # # # #     final_daily = df.groupby("day", as_index=False).agg({
# # # # #         "total_qty": "sum"
# # # # #     })

# # # # #     return final_daily



# # # # # from datetime import datetime
# # # # # from app.db import read_sql
# # # # # from app.queries import DAY_AGG_SQL
# # # # # from app.config import settings
# # # # # import pandas as pd

# # # # # def fetch_day_aggregates(start_date: str, end_date: str):
# # # # #     # Load daily data grouped by bill_date
# # # # #     query = DAY_AGG_SQL.format(
# # # # #         schema=settings.TARGET_SCHEMA,
# # # # #         sales_table=settings.SOURCE_TABLE1,     # generic_sales_history
# # # # #         assort_table=settings.SOURCE_TABLE2     # generic_final_assortment
# # # # #     )

# # # # #     params = {"start_date": start_date, "end_date": end_date}

# # # # #     df = read_sql(query, params)

# # # # #     # Remove negative quantities
# # # # #     df = df[df["total_qty"] >= 0]

# # # # #     # Final daily aggregation (sum of all assortments)
# # # # #     final_daily = df.groupby("day", as_index=False).agg({
# # # # #         "total_qty": "sum"
# # # # #     })

# # # # #     return final_daily


# # # # from datetime import datetime, timedelta
# # # # import pandas as pd
# # # # from app.db import read_sql
# # # # from app.queries import DAY_AGG_SQL
# # # # from app.config import settings


# # # # def fetch_day_aggregates(start_date: str = None, end_date: str = None):
# # # #     """Fetch aggregated daily sales qty from DB."""

# # # #     # Default to last 365 days if dates not provided
# # # #     if start_date is None or end_date is None:
# # # #         end = datetime.utcnow().date()
# # # #         start = end - timedelta(days=365)
# # # #         start_date = start.isoformat()
# # # #         end_date = end.isoformat()

# # # #     print(f"\n[INGEST] Fetching DB rows from {start_date} → {end_date}")

# # # #     # Format SQL query with schema + table names from .env
# # # #     query = DAY_AGG_SQL.format(
# # # #         schema=settings.TARGET_SCHEMA,
# # # #         sales_table=settings.SOURCE_TABLE1,
# # # #         assort_table=settings.SOURCE_TABLE2
# # # #     )

# # # #     params = {"start_date": start_date, "end_date": end_date}

# # # #     # Execute SQL
# # # #     df = read_sql(query, params)
# # # #     print("[INGEST] Raw rows returned:", df.shape)

# # # #     # If no rows → return empty safe DataFrame
# # # #     if df.empty:
# # # #         print("[INGEST] WARNING: No sales data returned for this date range!")
# # # #         return pd.DataFrame(columns=["day", "total_qty"])

# # # #     # Remove negative qty
# # # #     df = df[df["total_qty"] >= 0]

# # # #     # Aggregate to DAILY totals (across all products)
# # # #     daily = df.groupby("day", as_index=False).agg({"total_qty": "sum"})
# # # #     print("[INGEST] Final daily aggregated shape:", daily.shape)

# # # #     return daily



# # # from datetime import datetime, timedelta
# # # import pandas as pd
# # # from app.db import read_sql
# # # from app.queries import DAY_AGG_SQL
# # # from app.config import settings


# # # def get_date_range_from_db():
# # #     q = f"""
# # #     SELECT 
# # #         MIN(bill_date)::date AS min_date,
# # #         MAX(bill_date)::date AS max_date
# # #     FROM {settings.TARGET_SCHEMA}.{settings.SOURCE_TABLE1};
# # #     """
# # #     df = read_sql(q)
# # #     return df['min_date'][0], df['max_date'][0]


# # # def fetch_day_aggregates(start_date=None, end_date=None):
# # #     # Auto detect available DB date range
# # #     db_min, db_max = get_date_range_from_db()
# # #     print(f"[DB RANGE] {db_min} → {db_max}")

# # #     if start_date is None or end_date is None:
# # #         start_date, end_date = db_min, db_max

# # #     print(f"[INGEST] Fetching {start_date} → {end_date}")

# # #     query = DAY_AGG_SQL.format(
# # #         schema=settings.TARGET_SCHEMA,
# # #         sales_table=settings.SOURCE_TABLE1,
# # #         assort_table=settings.SOURCE_TABLE2
# # #     )

# # #     df = read_sql(query, {"start_date": start_date, "end_date": end_date})
# # #     print("[INGEST] Raw rows =", df.shape)

# # #     # If nothing found → fallback to full range
# # #     if df.empty:
# # #         print("[INGEST WARNING] Empty range → fallback to full DB range")
# # #         df = read_sql(query, {"start_date": db_min, "end_date": db_max})

# # #     if df.empty:
# # #         raise Exception("No usable sales rows found in DB.")

# # #     # Remove negative qty
# # #     df = df[df["total_qty"] >= 0]

# # #     # DAILY AGG
# # #     daily = df.groupby("day", as_index=False)["total_qty"].sum()
# # #     print("[INGEST] Final daily shape =", daily.shape)

# # #     return daily



# # from datetime import datetime, timedelta
# # import pandas as pd
# # from app.db import read_sql
# # from app.queries import DAY_AGG_SQL
# # from app.config import settings
# # from app.logger import logger


# # def get_date_range_from_db():
# #     q = f"""
# #     SELECT 
# #         MIN(bill_date)::date AS min_date,
# #         MAX(bill_date)::date AS max_date
# #     FROM {settings.TARGET_SCHEMA}.{settings.SOURCE_TABLE1};
# #     """

# #     df = read_sql(q)
# #     logger.info(f"DB RANGE → {df['min_date'][0]} → {df['max_date'][0]}")
# #     return df["min_date"][0], df["max_date"][0]


# # def fetch_day_aggregates(start_date=None, end_date=None):
# #     db_min, db_max = get_date_range_from_db()

# #     if start_date is None or end_date is None:
# #         start_date, end_date = db_min, db_max

# #     logger.info(f"[INGEST] Fetching sales between {start_date} → {end_date}")

# #     query = DAY_AGG_SQL.format(
# #         schema=settings.TARGET_SCHEMA,
# #         sales_table=settings.SOURCE_TABLE1,
# #         assort_table=settings.SOURCE_TABLE2
# #     )

# #     df = read_sql(query, {"start_date": start_date, "end_date": end_date})
# #     logger.info(f"[INGEST] Raw rows fetched: {df.shape}")

# #     if df.empty:
# #         logger.warning("[INGEST] Empty dataframe from DB, fallback → FULL DB RANGE")
# #         df = read_sql(query, {"start_date": db_min, "end_date": db_max})

# #     if df.empty:
# #         logger.error("[INGEST] Even full DB returned NO DATA!")
# #         return pd.DataFrame(columns=["day", "total_qty"])

# #     df = df[df["total_qty"] >= 0]

# #     daily = df.groupby("day", as_index=False)["total_qty"].sum()
# #     logger.info(f"[INGEST] Daily aggregated → {daily.shape}")

# #     return daily



# from datetime import datetime
# import pandas as pd
# from app.db import read_sql
# from app.queries import DAY_AGG_SQL
# from app.config import settings
# from app.logger import logger


# def get_date_range_from_db():
#     q = f"""
#     SELECT 
#         MIN(bill_date)::date AS min_date,
#         MAX(bill_date)::date AS max_date
#     FROM {settings.TARGET_SCHEMA}.{settings.SOURCE_TABLE1};
#     """

#     df = read_sql(q)
#     logger.info(f"DB RANGE → {df['min_date'][0]} → {df['max_date'][0]}")
#     return df['min_date'][0], df['max_date'][0]


# def fetch_day_aggregates(start_date=None, end_date=None):
#     db_min, db_max = get_date_range_from_db()

#     if start_date is None or end_date is None:
#         start_date, end_date = db_min, db_max

#     logger.info(f"[INGEST] Fetching sales between {start_date} → {end_date}")

#     query = DAY_AGG_SQL.format(
#         schema=settings.TARGET_SCHEMA,
#         sales_table=settings.SOURCE_TABLE1,
#         assort_table=settings.SOURCE_TABLE2
#     )

#     df = read_sql(query, {"start_date": start_date, "end_date": end_date})
#     logger.info(f"[INGEST] Raw rows fetched: {df.shape}")

#     if df.empty:
#         logger.error("NO DATA FOUND FOR DATE RANGE")
#         return pd.DataFrame(columns=["day", "site_code", "assortment_name", "total_qty"])

#     # Remove negative qty
#     df = df[df["total_qty"] >= 0]

#     # ASSORTMENT-WISE DAILY AGG
#     daily = df.groupby(
#         ["day", "site_code", "assortment_name"], as_index=False
#     )["total_qty"].sum()

#     logger.info(f"[INGEST] Daily aggregated → {daily.shape}")

#     return daily



# ingest.py
from datetime import datetime
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

    # Respect user-provided boundaries
    if start_date is None:
        start_date = db_min

    if end_date is None:
        end_date = db_max

    logger.info(f"[INGEST] Fetching sales from {start_date} → {end_date}")

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

    # As per your final logic: assortment-wise daily
    out = df.groupby(["day", "site_code", "assortment_name"], as_index=False)["total_qty"].sum()
    return out

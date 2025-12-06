# import logging
# import pandas as pd
# from datetime import datetime
# from sqlalchemy import text
# from app.db import get_engine
# from app.config import settings

# logger = logging.getLogger("forecast-app")

# TABLE_NAME = "forecast_results_new"
# SCHEMA = settings.TARGET_SCHEMA


# def write_forecast_to_db(df: pd.DataFrame, prediction_type: str):
#     try:
#         engine = get_engine()

#         logger.info(f"[DB] Writing {len(df)} rows → {SCHEMA}.{TABLE_NAME}")

#         # Create table if not exists
#         with engine.begin() as conn:
#             conn.execute(text(f"""
#                 CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE_NAME} (
#                     site_code INT,
#                     assortment_name VARCHAR,
#                     month VARCHAR(20),
#                     predicted_qty DOUBLE PRECISION,
#                     prediction_date DATE,
#                     prediction_type VARCHAR(20),
#                     created_at TIMESTAMP DEFAULT NOW()
#                 );
#             """))

#         df["created_at"] = datetime.now()

#         df.to_sql(
#             TABLE_NAME,
#             engine,
#             schema=SCHEMA,
#             if_exists="append",
#             index=False,
#             method="multi",
#             chunksize=1000
#         )

#         logger.info("[DB] Insert successful")

#     except Exception as e:
#         logger.error("[DB ERROR]", exc_info=True)
#         raise



import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from app.db import get_engine
from app.config import settings

logger = logging.getLogger("forecast-app")

TABLE_NAME = settings.RESULT_TABLE
SCHEMA = settings.TARGET_SCHEMA


# ===========================================
# 🔥 AUTO SCHEMA MIGRATION (NO MORE ERRORS)
# ===========================================
def ensure_table_schema(engine, schema, table):
    with engine.begin() as conn:

        # 1️⃣ Create table if not exists
        conn.execute(text(f"""
            CREATE TABLE IF NOT EXISTS {schema}.{table} (
                site_code INT,
                assortment_name VARCHAR,
                month VARCHAR(20),
                week VARCHAR(20),
                predicted_qty DOUBLE PRECISION,
                prediction_date DATE,
                prediction_type VARCHAR(20),
                created_at TIMESTAMP DEFAULT NOW()
            );
        """))

        # 2️⃣ Auto-add missing columns (safe)
        conn.execute(text(f"ALTER TABLE {schema}.{table} ADD COLUMN IF NOT EXISTS month VARCHAR(20);"))
        conn.execute(text(f"ALTER TABLE {schema}.{table} ADD COLUMN IF NOT EXISTS week VARCHAR(20);"))
        conn.execute(text(f"ALTER TABLE {schema}.{table} ADD COLUMN IF NOT EXISTS predicted_qty DOUBLE PRECISION;"))
        conn.execute(text(f"ALTER TABLE {schema}.{table} ADD COLUMN IF NOT EXISTS prediction_date DATE;"))
        conn.execute(text(f"ALTER TABLE {schema}.{table} ADD COLUMN IF NOT EXISTS prediction_type VARCHAR(20);"))
        conn.execute(text(f"ALTER TABLE {schema}.{table} ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();"))

        logger.info("[DB] Schema verified & updated successfully.")


# ===========================================
# 🔥 FINAL WRITER FUNCTION (UPSERT LOGIC)
# ===========================================
def write_forecast_to_db(df: pd.DataFrame, prediction_type: str):
    engine = get_engine()
    schema = settings.TARGET_SCHEMA
    table = TABLE_NAME

    # 🟢 Auto add missing table/columns BEFORE writing
    ensure_table_schema(engine, schema, table)

    df = df.copy()
    df["prediction_type"] = prediction_type
    df["created_at"] = datetime.now()

    # Ensure required columns exist in dataframe
    if "month" not in df.columns:
        df["month"] = None
    if "week" not in df.columns:
        df["week"] = None

    # =======================================
    # 2️⃣ DELETE ONLY MATCHING ROWS (UPSERT)
    # =======================================
    with engine.begin() as conn:

        for _, row in df.iterrows():

            if prediction_type == "monthly":
                conn.execute(text(f"""
                    DELETE FROM {schema}.{table}
                    WHERE site_code = :site
                    AND assortment_name = :asmt
                    AND month = :month
                    AND prediction_type = 'monthly';
                """), {
                    "site": row["site_code"],
                    "asmt": row["assortment_name"],
                    "month": row["month"]
                })

            elif prediction_type == "weekly":
                conn.execute(text(f"""
                    DELETE FROM {schema}.{table}
                    WHERE site_code = :site
                    AND assortment_name = :asmt
                    AND week = :week
                    AND prediction_type = 'weekly';
                """), {
                    "site": row["site_code"],
                    "asmt": row["assortment_name"],
                    "week": row["week"]
                })

    # =======================================
    # 3️⃣ INSERT (APPEND)
    # =======================================
    df[[
        "site_code",
        "assortment_name",
        "month",
        "week",
        "predicted_qty",
        "prediction_date",
        "prediction_type",
        "created_at"
    ]].to_sql(
        table,
        engine,
        schema=schema,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000
    )

    logger.info(f"[DB] Successfully inserted {len(df)} rows for {prediction_type}")

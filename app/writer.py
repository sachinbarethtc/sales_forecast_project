# # # # # from app.db import get_engine
# # # # # import pandas as pd
# # # # # from app.config import settings
# # # # # from sqlalchemy import text


# # # # # def write_forecast_to_db(forecast_df: pd.DataFrame, freq: str, created_by: str = "system"):
# # # # #     # """
# # # # #     # Writes forecast results into the results table.
# # # # #     # forecast_df must contain columns:
# # # # #     #     - day
# # # # #     #     - yhat
# # # # #     #     - yhat_lower
# # # # #     #     - yhat_upper
# # # # #     # """

# # # # #     # engine = get_engine()

# # # # #     # # Using uppercase env variables as per updated config.py
# # # # #     # schema = settings.TARGET_SCHEMA
# # # # #     # table = settings.RESULT_TABLE

# # # # #     # with engine.begin() as conn:

# # # # #     #     # Create table if not exists
# # # # #     #     conn.execute(text(f"""
# # # # #     #         CREATE TABLE IF NOT EXISTS {schema}.{table} (
# # # # #     #             day date,
# # # # #     #             freq varchar(20),
# # # # #     #             yhat double precision,
# # # # #     #             yhat_lower double precision,
# # # # #     #             yhat_upper double precision,
# # # # #     #             created_at timestamp default now(),
# # # # #     #             created_by varchar(50)
# # # # #     #         );
# # # # #     #     """))

# # # # #     #     # Clear old forecast of same frequency (monthly/weekly)
# # # # #     #     conn.execute(
# # # # #     #         text(f"DELETE FROM {schema}.{table} WHERE freq = :freq"),
# # # # #     #         {"freq": freq}
# # # # #     #     )

# # # # #     #     # Prepare dataframe for insertion
# # # # #     #     df = forecast_df.copy()
# # # # #     #     df["freq"] = freq
# # # # #     #     df["created_by"] = created_by

# # # # #     #     # Insert new forecast
# # # # #     #     df.to_sql(
# # # # #     #         table,
# # # # #     #         con=engine,
# # # # #     #         schema=schema,
# # # # #     #         if_exists="append",
# # # # #     #         index=False,
# # # # #     #         method="multi"
# # # # #     #     )

# # # # #     return True



# # # # import pandas as pd
# # # # from sqlalchemy import text
# # # # from app.db import get_engine
# # # # from app.config import settings


# # # # def write_forecast_to_db(df: pd.DataFrame, freq: str, created_by="system"):
# # # #     engine = get_engine()
# # # #     schema = settings.TARGET_SCHEMA
# # # #     table = settings.RESULT_TABLE

# # # #     with engine.begin() as conn:
# # # #         conn.execute(text(f"""
# # # #             CREATE TABLE IF NOT EXISTS {schema}.{table} (
# # # #                 day date,
# # # #                 freq varchar,
# # # #                 yhat double precision,
# # # #                 yhat_lower double precision,
# # # #                 yhat_upper double precision,
# # # #                 created_at timestamp default now(),
# # # #                 created_by varchar
# # # #             );
# # # #         """))

# # # #         conn.execute(
# # # #             text(f"DELETE FROM {schema}.{table} WHERE freq = :freq"),
# # # #             {"freq": freq}
# # # #         )

# # # #         df2 = df.copy()
# # # #         df2["freq"] = freq
# # # #         df2["created_by"] = created_by

# # # #         df2.to_sql(table, engine, schema=schema, if_exists="append", index=False, method="multi")



# # # import pandas as pd
# # # from sqlalchemy import text
# # # from app.db import get_engine
# # # from app.config import settings
# # # from app.logger import logger


# # # def write_forecast_to_db(df: pd.DataFrame, freq: str, created_by="system"):
# # #     logger.info(f"[DB WRITE] Writing {len(df)} rows for freq={freq}")

# # #     engine = get_engine()
# # #     schema = settings.TARGET_SCHEMA
# # #     table = settings.RESULT_TABLE

# # #     with engine.begin() as conn:
# # #         conn.execute(text(f"""
# # #             CREATE TABLE IF NOT EXISTS {schema}.{table} (
# # #                 day date,
# # #                 freq varchar,
# # #                 yhat double precision,
# # #                 yhat_lower double precision,
# # #                 yhat_upper double precision,
# # #                 created_at timestamp default now(),
# # #                 created_by varchar
# # #             );
# # #         """))

# # #         conn.execute(text(f"DELETE FROM {schema}.{table} WHERE freq = :freq"),
# # #                      {"freq": freq})

# # #     df2 = df.copy()
# # #     df2["freq"] = freq
# # #     df2["created_by"] = created_by

# # #     df2.to_sql(table, engine, schema=schema, if_exists="append",
# # #                index=False, method="multi")

# # #     logger.info("[DB WRITE] Completed insertion.")



# # import pandas as pd
# # from sqlalchemy import text
# # from app.db import get_engine
# # from app.config import settings
# # from app.logger import logger


# # def write_assortment_forecast(df: pd.DataFrame, prediction_type: str):

# #     engine = get_engine()
# #     schema = settings.TARGET_SCHEMA
# #     table = settings.RESULT_TABLE  # example: forecast_results_assortment

# #     logger.info(f"[DB WRITE] Writing {len(df)} rows → {schema}.{table}")

# #     with engine.begin() as conn:
# #         conn.execute(text(f"""
# #             CREATE TABLE IF NOT EXISTS {schema}.{table} (
# #                 site_code INT,
# #                 assortment_name VARCHAR,
# #                 month VARCHAR(10),
# #                 predicted_qty DOUBLE PRECISION,
# #                 prediction_date DATE,
# #                 prediction_type VARCHAR(20),
# #                 created_at TIMESTAMP DEFAULT NOW()
# #             );
# #         """))

# #     df.to_sql(table, engine, schema=schema,
# #               if_exists="append", index=False, method="multi")

# #     logger.info("[DB WRITE] Insert completed.")


# import logging
# import pandas as pd
# from datetime import datetime
# from sqlalchemy import text

# logger = logging.getLogger("forecast-app")

# TABLE_NAME = "forecast_results"
# SCHEMA = "mbazaar_sandbox"


# def write_forecast_to_db(df: pd.DataFrame, freq: str):
#     """
#     Convert assortment-level output into global table format.
#     Table expects: day, freq, yhat, yhat_lower, yhat_upper, created_at, created_by
#     """

#     try:
#         logger.info(f"[DB] Preparing {len(df)} rows for insert → {SCHEMA}.{TABLE_NAME}")

#         out = pd.DataFrame()

#         # REQUIRED COLUMNS IN FINAL TABLE
#         out["day"] = df["month"].astype(str) + "-01"
#         out["day"] = pd.to_datetime(out["day"]) + pd.offsets.MonthEnd(0)

#         out["freq"] = freq.lower()
#         out["yhat"] = df["predicted_qty"].astype(float)

#         # For now we assume no CI, set same value
#         out["yhat_lower"] = out["yhat"] * 0.8
#         out["yhat_upper"] = out["yhat"] * 1.2

#         out["created_at"] = datetime.now()
#         out["created_by"] = "system"

#         logger.info(f"[DB] Final converted rows → {out.shape}")

#         from app.db import engine

#         out.to_sql(
#             TABLE_NAME,
#             engine,
#             schema=SCHEMA,
#             if_exists="append",
#             index=False,
#             method="multi",
#             chunksize=500
#         )

#         logger.info("[DB] Insert successful")

#     except Exception as e:
#         logger.error(f"[DB ERROR] {str(e)}", exc_info=True)
#         raise


import logging
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from app.db import get_engine
from app.config import settings

logger = logging.getLogger("forecast-app")

TABLE_NAME = "forecast_results_assortment"
SCHEMA = settings.TARGET_SCHEMA


def write_forecast_to_db(df: pd.DataFrame, prediction_type: str):
    try:
        engine = get_engine()

        logger.info(f"[DB] Writing {len(df)} rows → {SCHEMA}.{TABLE_NAME}")

        # Create table if not exists
        with engine.begin() as conn:
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {SCHEMA}.{TABLE_NAME} (
                    site_code INT,
                    assortment_name VARCHAR,
                    month VARCHAR(20),
                    predicted_qty DOUBLE PRECISION,
                    prediction_date DATE,
                    prediction_type VARCHAR(20),
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """))

        df["created_at"] = datetime.now()

        df.to_sql(
            TABLE_NAME,
            engine,
            schema=SCHEMA,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

        logger.info("[DB] Insert successful")

    except Exception as e:
        logger.error("[DB ERROR]", exc_info=True)
        raise

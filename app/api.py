# # # # # # # # # from fastapi import FastAPI, HTTPException
# # # # # # # # # from app.models.schemas import ForecastRequest
# # # # # # # # # from app.ingest import fetch_day_aggregates
# # # # # # # # # from app.forecast import forecast
# # # # # # # # # from app.writer import write_forecast_to_db
# # # # # # # # # import pandas as pd
# # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # app = FastAPI(title="Sales Forecast API - ML Version")


# # # # # # # # # def _get_window(req: ForecastRequest):
# # # # # # # # #     if req.start_date and req.end_date:
# # # # # # # # #         return req.start_date, req.end_date
    
# # # # # # # # #     # end = datetime.utcnow().date()
# # # # # # # # #     # start = end - timedelta(days=365)
# # # # # # # # #     start = datetime(2022, 4, 1).date()
# # # # # # # # #     end = datetime(2023, 4, 1).date()
# # # # # # # # #     return start.isoformat(), end.isoformat()


# # # # # # # # # @app.post("/forecast/monthly")
# # # # # # # # # def monthly_forecast(req: ForecastRequest):
# # # # # # # # #     try:
# # # # # # # # #         start_date, end_date = _get_window(req)

# # # # # # # # #         daily = fetch_day_aggregates(start_date, end_date)

# # # # # # # # #         # Convert to monthly series
# # # # # # # # #         daily["day"] = pd.to_datetime(daily["day"])
# # # # # # # # #         monthly = daily.set_index("day").resample("M").sum().reset_index()

# # # # # # # # #         periods = req.horizon * 30  # months → days

# # # # # # # # #         # fc = forecast(monthly, horizon_days=periods, method="xgboost")
# # # # # # # # #         fc = forecast(monthly, horizon_days=periods)


# # # # # # # # #         write_forecast_to_db(fc, freq="monthly")

# # # # # # # # #         return {"status": "success", "rows": len(fc)}

# # # # # # # # #     except Exception as e:
# # # # # # # # #         raise HTTPException(status_code=500, detail=str(e))


# # # # # # # # # @app.post("/forecast/weekly")
# # # # # # # # # def weekly_forecast(req: ForecastRequest):
# # # # # # # # #     try:
# # # # # # # # #         start_date, end_date = _get_window(req)

# # # # # # # # #         daily = fetch_day_aggregates(start_date, end_date)

# # # # # # # # #         daily["day"] = pd.to_datetime(daily["day"])
# # # # # # # # #         weekly = daily.set_index("day").resample("W-MON").sum().reset_index()

# # # # # # # # #         periods = req.horizon * 7  # weeks → days

# # # # # # # # #         # fc = forecast(weekly, horizon_days=periods, method="xgboost")
# # # # # # # # #         fc = forecast(weekly, horizon_days=periods)


# # # # # # # # #         write_forecast_to_db(fc, freq="weekly")

# # # # # # # # #         return {"status": "success", "rows": len(fc)}

# # # # # # # # #     except Exception as e:
# # # # # # # # #         raise HTTPException(status_code=500, detail=str(e))



# # # # # # # # from fastapi import FastAPI, HTTPException
# # # # # # # # from app.models.schemas import ForecastRequest
# # # # # # # # from app.ingest import fetch_day_aggregates
# # # # # # # # from app.forecast import forecast
# # # # # # # # from app.writer import write_forecast_to_db
# # # # # # # # import pandas as pd

# # # # # # # # app = FastAPI(title="Sales Forecast API - Final Version")


# # # # # # # # @app.post("/forecast/monthly")
# # # # # # # # def monthly(req: ForecastRequest):
# # # # # # # #     try:
# # # # # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)

# # # # # # # #         daily["day"] = pd.to_datetime(daily["day"])
# # # # # # # #         monthly = daily.set_index("day").resample("ME").sum().reset_index()

# # # # # # # #         periods = req.horizon * 30

# # # # # # # #         fc = forecast(monthly, horizon_days=periods)
# # # # # # # #         write_forecast_to_db(fc, "monthly")
# # # # # # # #         return {"status": "success", "rows": len(fc)}
# # # # # # # #     except Exception as e:
# # # # # # # #         raise HTTPException(500, str(e))


# # # # # # # # @app.post("/forecast/weekly")
# # # # # # # # def weekly(req: ForecastRequest):
# # # # # # # #     try:
# # # # # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)

# # # # # # # #         daily["day"] = pd.to_datetime(daily["day"])
# # # # # # # #         weekly = daily.set_index("day").resample("W-MON").sum().reset_index()

# # # # # # # #         periods = req.horizon * 7

# # # # # # # #         fc = forecast(weekly, horizon_days=periods)
# # # # # # # #         write_forecast_to_db(fc, "weekly")
# # # # # # # #         return {"status": "success", "rows": len(fc)}
# # # # # # # #     except Exception as e:
# # # # # # # #         raise HTTPException(500, str(e))



# # # # # # # from fastapi import FastAPI, HTTPException
# # # # # # # from app.models.schemas import ForecastRequest
# # # # # # # from app.ingest import fetch_day_aggregates
# # # # # # # from app.forecast import forecast
# # # # # # # from app.writer import write_forecast_to_db
# # # # # # # from app.logger import logger
# # # # # # # import pandas as pd

# # # # # # # app = FastAPI(title="Sales Forecast API (Logged)")


# # # # # # # @app.post("/forecast/monthly")
# # # # # # # def monthly(req: ForecastRequest):
# # # # # # #     try:
# # # # # # #         logger.info(f"[API] Monthly forecast request: {req}")

# # # # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)

# # # # # # #         daily["day"] = pd.to_datetime(daily["day"])
# # # # # # #         monthly = daily.set_index("day").resample("ME").sum().reset_index()

# # # # # # #         logger.info(f"[API] Monthly DF shape = {monthly.shape}")

# # # # # # #         if monthly.empty:
# # # # # # #             logger.error("[API] Monthly aggregated data EMPTY")
# # # # # # #             raise Exception("Monthly data empty")

# # # # # # #         periods = req.horizon * 30

# # # # # # #         fc = forecast(monthly, horizon_days=periods)
# # # # # # #         write_forecast_to_db(fc, "monthly")

# # # # # # #         return {"status": "success", "rows": len(fc)}

# # # # # # #     except Exception as e:
# # # # # # #         logger.exception(e)
# # # # # # #         raise HTTPException(500, str(e))


# # # # # # # @app.post("/forecast/weekly")
# # # # # # # def weekly(req: ForecastRequest):
# # # # # # #     try:
# # # # # # #         logger.info(f"[API] Weekly forecast request: {req}")

# # # # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)

# # # # # # #         daily["day"] = pd.to_datetime(daily["day"])
# # # # # # #         weekly = daily.set_index("day").resample("W-MON").sum().reset_index()

# # # # # # #         logger.info(f"[API] Weekly DF shape = {weekly.shape}")

# # # # # # #         if weekly.empty:
# # # # # # #             logger.error("[API] Weekly aggregated data EMPTY")
# # # # # # #             raise Exception("Weekly data empty")

# # # # # # #         periods = req.horizon * 7

# # # # # # #         fc = forecast(weekly, horizon_days=periods)
# # # # # # #         write_forecast_to_db(fc, "weekly")

# # # # # # #         return {"status": "success", "rows": len(fc)}

# # # # # # #     except Exception as e:
# # # # # # #         logger.exception(e)
# # # # # # #         raise HTTPException(500, str(e))



# # # # # # from fastapi import FastAPI, HTTPException
# # # # # # from app.models.schemas import ForecastRequest
# # # # # # from app.ingest import fetch_day_aggregates
# # # # # # from app.forecast import forecast
# # # # # # from app.writer import write_forecast_to_db
# # # # # # from app.logger import logger
# # # # # # import pandas as pd

# # # # # # app = FastAPI(title="Sales Forecast API (Stable Version)")


# # # # # # # -----------------------------------
# # # # # # # MONTHLY FORECAST (Daily → Model → Monthly)
# # # # # # # -----------------------------------
# # # # # # @app.post("/forecast/monthly")
# # # # # # def monthly(req: ForecastRequest):
# # # # # #     try:
# # # # # #         logger.info(f"[API] Monthly forecast request: {req}")

# # # # # #         # 1️⃣ Fetch DAILY data (ALWAYS for model training)
# # # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)
# # # # # #         daily["day"] = pd.to_datetime(daily["day"])

# # # # # #         if daily.empty:
# # # # # #             raise Exception("No daily sales data found.")

# # # # # #         logger.info(f"[API] Daily DF shape = {daily.shape}")

# # # # # #         # 2️⃣ Train + Forecast DAILY
# # # # # #         periods = req.horizon * 30  # horizon months → days
# # # # # #         daily_fc = forecast(daily, horizon_days=periods)

# # # # # #         logger.info(f"[API] Daily forecast result shape = {daily_fc.shape}")

# # # # # #         # 3️⃣ Convert DAILY forecast → MONTHLY forecast
# # # # # #         daily_fc["day"] = pd.to_datetime(daily_fc["day"])
# # # # # #         monthly_fc = (
# # # # # #             daily_fc.set_index("day")
# # # # # #             .resample("ME")
# # # # # #             .sum()
# # # # # #             .reset_index()
# # # # # #         )

# # # # # #         logger.info(f"[API] Final monthly forecast shape = {monthly_fc.shape}")

# # # # # #         if monthly_fc.empty:
# # # # # #             raise Exception("Monthly forecast result is empty.")

# # # # # #         # 4️⃣ Save to DB
# # # # # #         write_forecast_to_db(monthly_fc, "monthly")

# # # # # #         return {"status": "success", "rows": len(monthly_fc)}

# # # # # #     except Exception as e:
# # # # # #         logger.exception(e)
# # # # # #         raise HTTPException(500, str(e))


# # # # # # # -----------------------------------
# # # # # # # WEEKLY FORECAST (Daily → Model → Weekly)
# # # # # # # -----------------------------------
# # # # # # @app.post("/forecast/weekly")
# # # # # # def weekly(req: ForecastRequest):
# # # # # #     try:
# # # # # #         logger.info(f"[API] Weekly forecast request: {req}")

# # # # # #         # 1️⃣ Fetch DAILY data
# # # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)
# # # # # #         daily["day"] = pd.to_datetime(daily["day"])

# # # # # #         if daily.empty:
# # # # # #             raise Exception("No daily sales data found.")

# # # # # #         logger.info(f"[API] Daily DF shape = {daily.shape}")

# # # # # #         # 2️⃣ Train + Forecast DAILY
# # # # # #         periods = req.horizon * 7  # horizon weeks → days
# # # # # #         daily_fc = forecast(daily, horizon_days=periods)

# # # # # #         logger.info(f"[API] Daily forecast result shape = {daily_fc.shape}")

# # # # # #         # 3️⃣ Convert DAILY forecast → WEEKLY forecast
# # # # # #         daily_fc["day"] = pd.to_datetime(daily_fc["day"])
# # # # # #         weekly_fc = (
# # # # # #             daily_fc.set_index("day")
# # # # # #             .resample("W-MON")
# # # # # #             .sum()
# # # # # #             .reset_index()
# # # # # #         )

# # # # # #         logger.info(f"[API] Final weekly forecast shape = {weekly_fc.shape}")

# # # # # #         if weekly_fc.empty:
# # # # # #             raise Exception("Weekly forecast result is empty.")

# # # # # #         # 4️⃣ Save to DB
# # # # # #         write_forecast_to_db(weekly_fc, "weekly")

# # # # # #         return {"status": "success", "rows": len(weekly_fc)}

# # # # # #     except Exception as e:
# # # # # #         logger.exception(e)
# # # # # #         raise HTTPException(500, str(e))



# # # # # from fastapi import FastAPI, HTTPException
# # # # # from app.models.schemas import ForecastRequest
# # # # # from app.ingest import fetch_day_aggregates
# # # # # # from app.forecast import forecast_one_assortment
# # # # # from app.forecast import forecast_one_assortment
# # # # # # from app.writer import write_assortment_forecast
# # # # # from app.writer import write_forecast_to_db
# # # # # from app.logger import logger
# # # # # import pandas as pd

# # # # # app = FastAPI(title="Assortment Forecast API")

# # # # # # ---------------------------------------------
# # # # # # MONTHLY FORECAST
# # # # # # ---------------------------------------------
# # # # # @app.post("/forecast/monthly")
# # # # # def forecast_monthly(req: ForecastRequest):
# # # # #     try:
# # # # #         logger.info(f"[API] Monthly forecast request: {req}")

# # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)
# # # # #         if daily.empty:
# # # # #             raise Exception("No sales data found.")

# # # # #         periods = req.horizon * 30  # monthly → daily horizon
# # # # #         all_results = []

# # # # #         for (site, asmt), group in daily.groupby(["site_code", "assortment_name"]):

# # # # #             logger.info(f"[MONTHLY] Forecasting site={site}, asmt={asmt}")

# # # # #             sub_df = group[["day", "total_qty"]]
# # # # #             fc = forecast_one_assortment(sub_df, periods)

# # # # #             # Add identifiers
# # # # #             fc["site_code"] = site
# # # # #             fc["assortment_name"] = asmt

# # # # #             # Convert daily forecast → monthly
# # # # #             fc["month"] = fc["day"].dt.strftime("%Y-%m")
# # # # #             fc["prediction_date"] = fc["month"] + "-01"
# # # # #             fc["prediction_type"] = "monthly"

# # # # #             # Aggregate monthly per assortment
# # # # #             monthly_fc = (
# # # # #                 fc.groupby(["site_code", "assortment_name", "month", "prediction_date", "prediction_type"],
# # # # #                            as_index=False)["predicted_qty"].sum()
# # # # #             )

# # # # #             all_results.append(monthly_fc)

# # # # #         final_df = pd.concat(all_results, ignore_index=True)

# # # # #         write_forecast_to_db(final_df, "monthly")
# # # # #         # write_forecast_to_db(final_df)


# # # # #         return {"status": "success", "rows": len(final_df)}

# # # # #     except Exception as e:
# # # # #         logger.exception(e)
# # # # #         raise HTTPException(500, str(e))


# # # # # # ---------------------------------------------
# # # # # # WEEKLY FORECAST
# # # # # # ---------------------------------------------
# # # # # @app.post("/forecast/weekly")
# # # # # def forecast_weekly(req: ForecastRequest):
# # # # #     try:
# # # # #         logger.info(f"[API] Weekly forecast request: {req}")

# # # # #         daily = fetch_day_aggregates(req.start_date, req.end_date)
# # # # #         if daily.empty:
# # # # #             raise Exception("No sales data found.")

# # # # #         periods = req.horizon * 7  # weekly → daily horizon
# # # # #         all_results = []

# # # # #         for (site, asmt), group in daily.groupby(["site_code", "assortment_name"]):

# # # # #             logger.info(f"[WEEKLY] Forecasting site={site}, asmt={asmt}")

# # # # #             sub_df = group[["day", "total_qty"]]
# # # # #             fc = forecast_one_assortment(sub_df, periods)

# # # # #             fc["site_code"] = site
# # # # #             fc["assortment_name"] = asmt

# # # # #             # Convert daily forecast → weekly (W-MON format)
# # # # #             fc["week_start"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
# # # # #             fc["prediction_date"] = fc["week_start"].dt.strftime("%Y-%m-%d")
# # # # #             fc["week"] = fc["week_start"].dt.strftime("%Y-%U")
# # # # #             fc["prediction_type"] = "weekly"

# # # # #             # Aggregate weekly qty
# # # # #             weekly_fc = (
# # # # #                 fc.groupby(["site_code", "assortment_name", "week", "prediction_date", "prediction_type"],
# # # # #                            as_index=False)["predicted_qty"].sum()
# # # # #             )

# # # # #             all_results.append(weekly_fc)

# # # # #         final_df = pd.concat(all_results, ignore_index=True)

# # # # #         write_forecast_to_db(final_df, "weekly")
# # # # #         # write_forecast_to_db(final_df)


# # # # #         return {"status": "success", "rows": len(final_df)}

# # # # #     except Exception as e:
# # # # #         logger.exception(e)
# # # # #         raise HTTPException(500, str(e))




# # # # import traceback
# # # # from fastapi import APIRouter, HTTPException
# # # # from pydantic import BaseModel
# # # # import pandas as pd
# # # # from datetime import datetime
# # # # from app.ingest import fetch_day_aggregates
# # # # from app.writer import write_forecast_to_db
# # # # from app.utils.forecast_engine import forecast_group

# # # # router = APIRouter()


# # # # # ==============================
# # # # # REQUEST MODEL
# # # # # ==============================
# # # # class ForecastRequest(BaseModel):
# # # #     start_date: str
# # # #     end_date: str
# # # #     horizon: int = 3  # number of periods (months/weeks)
# # # #     method: str = "auto"  # not used, but kept for compatibility


# # # # # ==============================
# # # # # BUILD FINAL TABLE FORMAT
# # # # # ==============================
# # # # def build_forecast_table(df, periods=3, prediction_type="monthly"):
# # # #     rows = []

# # # #     grouped = df.groupby(["site_code", "assortment_name"])

# # # #     for (site, asmt), g in grouped:

# # # #         try:
# # # #             sar, xgb = forecast_group(
# # # #                 g,
# # # #                 freq="monthly" if prediction_type == "monthly" else "weekly",
# # # #                 periods=periods
# # # #             )
# # # #         except Exception as e:
# # # #             print("FORECAST ERROR FOR:", site, asmt, e)
# # # #             continue

# # # #         # Prefer XGBoost model
# # # #         forecast = xgb if xgb is not None else sar
# # # #         if forecast is None:
# # # #             continue

# # # #         for dt, qty in forecast.items():

# # # #             # month format
# # # #             if prediction_type == "monthly":
# # # #                 month_val = dt.strftime("%Y-%m")
# # # #             else:
# # # #                 month_val = dt.strftime("%Y-W%V")   # weekly format

# # # #             rows.append({
# # # #                 "site_code": str(site),
# # # #                 "assortment_name": str(asmt),
# # # #                 "month": month_val,
# # # #                 "predicted_qty": round(float(qty), 4),
# # # #                 "prediction_date": dt.strftime("%Y-%m-%d"),
# # # #                 "prediction_type": prediction_type
# # # #             })

# # # #     return pd.DataFrame(rows)


# # # # # ==============================
# # # # # MONTHLY FORECAST API
# # # # # ==============================
# # # # @router.post("/forecast/monthly")
# # # # def forecast_monthly(req: ForecastRequest):
# # # #     try:
# # # #         print(f"[API] Monthly forecast request → {req}")

# # # #         daily_df = fetch_day_aggregates(req.start_date, req.end_date)
# # # #         if daily_df.empty:
# # # #             raise Exception("No sales data found for given date range")

# # # #         print("[API] Running monthly forecasting…")

# # # #         final_df = build_forecast_table(
# # # #             daily_df,
# # # #             periods=req.horizon,
# # # #             prediction_type="monthly"
# # # #         )

# # # #         if final_df.empty:
# # # #             raise Exception("Forecast table is empty")

# # # #         write_forecast_to_db(final_df, prediction_type="monthly")

# # # #         return {
# # # #             "status": "success",
# # # #             "rows_inserted": len(final_df),
# # # #             "sample_output": final_df.head(5).to_dict(orient="records"),
# # # #         }

# # # #     except Exception as e:
# # # #         print("ERROR:", e)
# # # #         traceback.print_exc()
# # # #         raise HTTPException(status_code=500, detail=str(e))


# # # # # ==============================
# # # # # WEEKLY FORECAST API
# # # # # ==============================
# # # # @router.post("/forecast/weekly")
# # # # def forecast_weekly(req: ForecastRequest):
# # # #     try:
# # # #         print(f"[API] Weekly forecast request → {req}")

# # # #         daily_df = fetch_day_aggregates(req.start_date, req.end_date)
# # # #         if daily_df.empty:
# # # #             raise Exception("No sales data found")

# # # #         print("[API] Running weekly forecasting…")

# # # #         final_df = build_forecast_table(
# # # #             daily_df,
# # # #             periods=req.horizon,
# # # #             prediction_type="weekly"
# # # #         )

# # # #         if final_df.empty:
# # # #             raise Exception("Forecast table is empty")

# # # #         write_forecast_to_db(final_df, prediction_type="weekly")

# # # #         return {
# # # #             "status": "success",
# # # #             "rows_inserted": len(final_df),
# # # #             "sample_output": final_df.head(5).to_dict(orient="records"),
# # # #         }

# # # #     except Exception as e:
# # # #         print("ERROR:", e)
# # # #         traceback.print_exc()
# # # #         raise HTTPException(status_code=500, detail=str(e))



# # # from fastapi import FastAPI, APIRouter, HTTPException
# # # from pydantic import BaseModel
# # # import pandas as pd
# # # from datetime import datetime
# # # from app.ingest import fetch_day_aggregates
# # # from app.forecast import forecast_one_assortment
# # # from app.writer import write_forecast_to_db

# # # # IMPORTANT — Create FastAPI App
# # # app = FastAPI(title="Assortment Forecast API")

# # # # APIRouter
# # # router = APIRouter()


# # # # ==============================
# # # # REQUEST MODEL
# # # # ==============================
# # # class ForecastRequest(BaseModel):
# # #     start_date: str | None = None
# # #     end_date: str | None = None
# # #     horizon: int = 3


# # # # ==============================
# # # # MONTHLY FORECAST API
# # # # ==============================
# # # @router.post("/forecast/monthly")
# # # def forecast_monthly(req: ForecastRequest):
# # #     try:
# # #         print(f"[API] Monthly forecast request → {req}")

# # #         daily_df = fetch_day_aggregates(req.start_date, req.end_date)
# # #         if daily_df.empty:
# # #             raise Exception("No sales data found")

# # #         # TOP-30 per site
# # #         totals = (
# # #             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
# # #             .sum()
# # #             .reset_index()
# # #         )

# # #         top30 = (
# # #             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
# # #             .groupby("site_code")
# # #             .head(30)
# # #         )

# # #         filtered_df = daily_df.merge(
# # #             top30[["site_code", "assortment_name"]],
# # #             on=["site_code", "assortment_name"],
# # #             how="inner"
# # #         )

# # #         periods = req.horizon * 30
# # #         all_results = []

# # #         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):

# # #             sub_df = g[["day", "total_qty"]]
# # #             fc = forecast_one_assortment(sub_df, periods)

# # #             fc["site_code"] = site
# # #             fc["assortment_name"] = asmt
# # #             fc["month"] = fc["day"].dt.strftime("%Y-%m")
# # #             fc["prediction_date"] = fc["month"] + "-01"
# # #             fc["prediction_type"] = "monthly"

# # #             monthly_fc = (
# # #                 fc.groupby(
# # #                     ["site_code", "assortment_name", "month", "prediction_date", "prediction_type"],
# # #                     as_index=False
# # #                 )["predicted_qty"].sum()
# # #             )

# # #             all_results.append(monthly_fc)

# # #         final_df = pd.concat(all_results, ignore_index=True)

# # #         write_forecast_to_db(final_df, prediction_type="monthly")

# # #         return {
# # #             "status": "success",
# # #             "rows": len(final_df),
# # #             "sample_output": final_df.head(5).to_dict(orient="records")
# # #         }

# # #     except Exception as e:
# # #         raise HTTPException(status_code=500, detail=str(e))



# # # # ==============================
# # # # WEEKLY FORECAST API
# # # # ==============================
# # # @router.post("/forecast/weekly")
# # # def forecast_weekly(req: ForecastRequest):
# # #     try:
# # #         print(f"[API] Weekly forecast request → {req}")

# # #         daily_df = fetch_day_aggregates(req.start_date, req.end_date)
# # #         if daily_df.empty:
# # #             raise Exception("No sales data found")

# # #         totals = (
# # #             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
# # #             .sum()
# # #             .reset_index()
# # #         )

# # #         top30 = (
# # #             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
# # #             .groupby("site_code")
# # #             .head(30)
# # #         )

# # #         filtered_df = daily_df.merge(
# # #             top30[["site_code", "assortment_name"]],
# # #             on=["site_code", "assortment_name"],
# # #             how="inner"
# # #         )

# # #         periods = req.horizon * 7
# # #         all_results = []

# # #         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):

# # #             sub_df = g[["day", "total_qty"]]
# # #             fc = forecast_one_assortment(sub_df, periods)

# # #             fc["site_code"] = site
# # #             fc["assortment_name"] = asmt
# # #             fc["week_start"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
# # #             fc["week"] = fc["week_start"].dt.strftime("%Y-W%U")
# # #             fc["prediction_date"] = fc["week_start"].dt.strftime("%Y-%m-%d")
# # #             fc["prediction_type"] = "weekly"

# # #             weekly_fc = (
# # #                 fc.groupby(
# # #                     ["site_code", "assortment_name", "week", "prediction_date", "prediction_type"],
# # #                     as_index=False
# # #                 )["predicted_qty"].sum()
# # #             )

# # #             all_results.append(weekly_fc)

# # #         final_df = pd.concat(all_results, ignore_index=True)

# # #         write_forecast_to_db(final_df, prediction_type="weekly")

# # #         return {
# # #             "status": "success",
# # #             "rows": len(final_df),
# # #             "sample_output": final_df.head(5).to_dict(orient="records")
# # #         }

# # #     except Exception as e:
# # #         raise HTTPException(status_code=500, detail=str(e))


# # # # IMPORTANT — Add router to FastAPI app
# # # app.include_router(router)


# # from fastapi import FastAPI, APIRouter, HTTPException
# # from pydantic import BaseModel
# # import pandas as pd
# # from datetime import datetime
# # from app.ingest import fetch_day_aggregates
# # from app.forecast import forecast_one_assortment
# # from app.writer import write_forecast_to_db

# # # FastAPI App + Router
# # app = FastAPI(title="Assortment Forecast API")
# # router = APIRouter()


# # # ==============================
# # # REQUEST MODEL
# # # ==============================
# # class ForecastRequest(BaseModel):
# #     start_date: str
# #     end_date: str
# #     horizon: int = 3   # Only used for model future window, NOT output range


# # # ==============================
# # # MONTHLY FORECAST API
# # # ==============================
# # @router.post("/forecast/monthly")
# # def forecast_monthly(req: ForecastRequest):
# #     try:
# #         print(f"[API] Monthly request → {req}")

# #         # 1️⃣ LOAD FULL HISTORY ALWAYS (NOT req.start_date)
# #         daily_df = fetch_day_aggregates(start_date=None, end_date=None)
# #         if daily_df.empty:
# #             raise Exception("No historical sales data found")

# #         # 2️⃣ TOP-30 PER SITE
# #         totals = (
# #             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
# #             .sum().reset_index()
# #         )

# #         top30 = (
# #             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
# #             .groupby("site_code").head(30)
# #         )

# #         filtered_df = daily_df.merge(
# #             top30[["site_code", "assortment_name"]],
# #             on=["site_code", "assortment_name"],
# #             how="inner"
# #         )

# #         # 3️⃣ DAILY FORECAST (Model needs daily)
# #         periods = req.horizon * 30
# #         all_results = []

# #         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):

# #             sub_df = g[["day", "total_qty"]]
# #             fc = forecast_one_assortment(sub_df, periods)

# #             fc["site_code"] = site
# #             fc["assortment_name"] = asmt

# #             # Convert Daily → Monthly
# #             fc["month"] = fc["day"].dt.strftime("%Y-%m")
# #             fc["prediction_date"] = fc["month"] + "-01"
# #             fc["prediction_type"] = "monthly"

# #             monthly_fc = (
# #                 fc.groupby(
# #                     ["site_code", "assortment_name", "month", "prediction_date", "prediction_type"],
# #                     as_index=False
# #                 )["predicted_qty"].sum()
# #             )

# #             all_results.append(monthly_fc)

# #         final_df = pd.concat(all_results, ignore_index=True)

# #         # 4️⃣ LIMIT FINAL OUTPUT STRICTLY TO start_date → end_date MONTHS
# #         start_period = pd.to_datetime(req.start_date).to_period("M")
# #         end_period = pd.to_datetime(req.end_date).to_period("M")

# #         allowed_months = [
# #             (start_period + i).strftime("%Y-%m")
# #             for i in range((end_period - start_period).n + 1)
# #         ]

# #         final_df = final_df[final_df["month"].isin(allowed_months)]

# #         # 5️⃣ SAVE
# #         write_forecast_to_db(final_df, prediction_type="monthly")

# #         return {
# #             "status": "success",
# #             "rows": len(final_df),
# #             "sample": final_df.head(10).to_dict(orient="records")
# #         }

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))



# # # ==============================
# # # WEEKLY FORECAST API
# # # ==============================
# # @router.post("/forecast/weekly")
# # def forecast_weekly(req: ForecastRequest):
# #     try:
# #         print(f"[API] Weekly request → {req}")

# #         # 1️⃣ ALWAYS LOAD FULL HISTORY
# #         daily_df = fetch_day_aggregates(start_date=None, end_date=None)
# #         if daily_df.empty:
# #             raise Exception("No historical sales data found")

# #         # 2️⃣ TOP-30 per site
# #         totals = (
# #             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
# #             .sum().reset_index()
# #         )

# #         top30 = (
# #             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
# #             .groupby("site_code").head(30)
# #         )

# #         filtered_df = daily_df.merge(
# #             top30[["site_code", "assortment_name"]],
# #             on=["site_code", "assortment_name"],
# #             how="inner"
# #         )

# #         periods = req.horizon * 7
# #         all_results = []

# #         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):

# #             sub_df = g[["day", "total_qty"]]
# #             fc = forecast_one_assortment(sub_df, periods)

# #             fc["site_code"] = site
# #             fc["assortment_name"] = asmt

# #             # Convert to weekly format
# #             fc["week_start"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
# #             fc["week"] = fc["week_start"].dt.strftime("%Y-W%U")
# #             fc["prediction_date"] = fc["week_start"].dt.strftime("%Y-%m-%d")
# #             fc["prediction_type"] = "weekly"

# #             weekly_fc = (
# #                 fc.groupby(
# #                     ["site_code", "assortment_name", "week", "prediction_date", "prediction_type"],
# #                     as_index=False
# #                 )["predicted_qty"].sum()
# #             )

# #             all_results.append(weekly_fc)

# #         final_df = pd.concat(all_results, ignore_index=True)

# #         # 4️⃣ STRICT WEEK FILTERING (start_date → end_date only)
# #         start = pd.to_datetime(req.start_date)
# #         end = pd.to_datetime(req.end_date)

# #         allowed_weeks = pd.date_range(start, end, freq="W-MON").strftime("%Y-W%U")

# #         final_df = final_df[final_df["week"].isin(allowed_weeks)]

# #         # 5️⃣ WRITE
# #         write_forecast_to_db(final_df, prediction_type="weekly")

# #         return {
# #             "status": "success",
# #             "rows": len(final_df),
# #             "sample": final_df.head(10).to_dict(orient="records")
# #         }

# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e))


# # # ADD ROUTER
# # app.include_router(router)



# from fastapi import FastAPI, APIRouter, HTTPException
# from pydantic import BaseModel
# import pandas as pd
# from datetime import datetime
# from app.ingest import fetch_day_aggregates
# from app.forecast import forecast_one_assortment
# from app.writer import write_forecast_to_db

# # FastAPI App + Router
# app = FastAPI(title="Assortment Forecast API")
# router = APIRouter()


# # ==============================
# # REQUEST MODEL
# # ==============================
# class ForecastRequest(BaseModel):
#     start_date: str
#     end_date: str
#     horizon: int = 3   # only future window, not output range


# # ==============================
# # MONTHLY FORECAST API
# # ==============================
# @router.post("/forecast/monthly")
# def forecast_monthly(req: ForecastRequest):
#     try:
#         print(f"[API] Monthly request → {req}")

#         # 1️⃣ Load FULL HISTORY (not user date)
#         daily_df = fetch_day_aggregates(None, None)
#         if daily_df.empty:
#             raise Exception("No historical sales data found")

#         # 2️⃣ Top-30 per site
#         totals = (
#             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
#             .sum().reset_index()
#         )

#         top30 = (
#             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
#             .groupby("site_code").head(30)
#         )

#         filtered_df = daily_df.merge(
#             top30[["site_code", "assortment_name"]],
#             on=["site_code", "assortment_name"],
#             how="inner"
#         )

#         # 3️⃣ Forecast horizon in DAYS
#         periods = req.horizon * 30
#         all_results = []

#         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):

#             sub_df = g[["day", "total_qty"]]
#             fc = forecast_one_assortment(sub_df, periods)

#             fc["site_code"] = site
#             fc["assortment_name"] = asmt

#             # Convert DAILY → MONTHLY
#             # fc["month"] = fc["day"].dt.strftime("%Y-%m")
#             # fc["prediction_date"] = fc["month"] + "-01"
#             fc["prediction_date"] = fc["day"].dt.to_period("M").dt.to_timestamp()

#             fc["prediction_type"] = "monthly"

#             monthly_fc = (
#                 fc.groupby(
#                     ["site_code", "assortment_name", "month", "prediction_date", "prediction_type"],
#                     as_index=False
#                 )["predicted_qty"].sum()
#             )

#             all_results.append(monthly_fc)

#         final_df = pd.concat(all_results, ignore_index=True)

#         # 4️⃣ Filter ONLY between user start_date → end_date
#         start_period = pd.to_datetime(req.start_date).to_period("M")
#         end_period = pd.to_datetime(req.end_date).to_period("M")

#         allowed_months = [
#             (start_period + i).strftime("%Y-%m")
#             for i in range((end_period - start_period).n + 1)
#         ]

#         final_df = final_df[final_df["month"].isin(allowed_months)]

#         # 5️⃣ Write to DB
#         write_forecast_to_db(final_df, "monthly")

#         return {
#             "status": "success",
#             "rows": len(final_df),
#             "sample_output": final_df.head(10).to_dict(orient="records")
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# # ==============================
# # WEEKLY FORECAST API
# # ==============================
# @router.post("/forecast/weekly")
# def forecast_weekly(req: ForecastRequest):
#     try:
#         print(f"[API] Weekly request → {req}")

#         # 1️⃣ Load FULL HISTORY
#         daily_df = fetch_day_aggregates(None, None)
#         if daily_df.empty:
#             raise Exception("No historical sales data found")

#         # 2️⃣ Top-30 assortments by site
#         totals = (
#             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
#             .sum().reset_index()
#         )
#         top30 = (
#             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
#             .groupby("site_code").head(30)
#         )

#         filtered_df = daily_df.merge(
#             top30[["site_code", "assortment_name"]],
#             on=["site_code", "assortment_name"],
#             how="inner"
#         )

#         periods = req.horizon * 7
#         all_results = []

#         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):

#             sub_df = g[["day", "total_qty"]]
#             fc = forecast_one_assortment(sub_df, periods)

#             fc["site_code"] = site
#             fc["assortment_name"] = asmt

#             # Convert DAILY → WEEKLY
#             # fc["week_start"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
#             # fc["week"] = fc["week_start"].dt.strftime("%Y-W%U")
#             # fc["prediction_date"] = fc["week_start"].dt.strftime("%Y-%m-%d")
#             fc["prediction_date"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
#             fc["prediction_date"] = fc["prediction_date"].dt.date

#             fc["prediction_type"] = "weekly"

#             weekly_fc = (
#                 fc.groupby(
#                     ["site_code", "assortment_name", "week", "prediction_date", "prediction_type"],
#                     as_index=False
#                 )["predicted_qty"].sum()
#             )

#             all_results.append(weekly_fc)

#         final_df = pd.concat(all_results, ignore_index=True)

#         # 4️⃣ Filter weeks strictly between start_date → end_date
#         start = pd.to_datetime(req.start_date)
#         end = pd.to_datetime(req.end_date)

#         allowed_weeks = pd.date_range(start, end, freq="W-MON").strftime("%Y-W%U")

#         final_df = final_df[final_df["week"].isin(allowed_weeks)]

#         # 5️⃣ Write
#         write_forecast_to_db(final_df, "weekly")

#         return {
#             "status": "success",
#             "rows": len(final_df),
#             "sample_output": final_df.head(10).to_dict(orient="records")
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# app.include_router(router)



from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from app.ingest import fetch_day_aggregates
from app.forecast import forecast_one_assortment
from app.writer import write_forecast_to_db

# FastAPI App + Router
app = FastAPI(title="Assortment Forecast API")
router = APIRouter()


# ==============================
# REQUEST MODEL
# ==============================
class ForecastRequest(BaseModel):
    start_date: str
    end_date: str
    horizon: int = 3


# ==============================
# MONTHLY FORECAST API
# ==============================
@router.post("/forecast/monthly")
def forecast_monthly(req: ForecastRequest):
    try:
        print(f"[API] Monthly request → {req}")

        # Load full recent sales history (ingest already limits to 365 days)
        daily_df = fetch_day_aggregates(None, None)
        if daily_df.empty:
            raise Exception("No historical sales data found")

        # Top-30 per site
        totals = (
            daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
            .sum().reset_index()
        )
        top30 = (
            totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
            .groupby("site_code").head(30)
        )

        filtered_df = daily_df.merge(
            top30[["site_code", "assortment_name"]],
            on=["site_code", "assortment_name"],
            how="inner"
        )

        periods = req.horizon * 30
        all_results = []

        for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):
            sub_df = g[["day", "total_qty"]]
            fc = forecast_one_assortment(sub_df, periods)

            fc["site_code"] = site
            fc["assortment_name"] = asmt

            # Convert daily → month start date
            fc["prediction_date"] = fc["day"].dt.to_period("M").dt.to_timestamp()
            fc["prediction_type"] = "monthly"

            monthly_fc = fc.groupby(
                ["site_code", "assortment_name", "prediction_date", "prediction_type"],
                as_index=False
            )["predicted_qty"].sum()

            all_results.append(monthly_fc)

        final_df = pd.concat(all_results, ignore_index=True)

        # Filter for requested output range
        start = pd.to_datetime(req.start_date)
        end = pd.to_datetime(req.end_date)
        final_df = final_df[
            (final_df["prediction_date"] >= start) &
            (final_df["prediction_date"] <= end)
        ]

        write_forecast_to_db(final_df, "monthly")

        return {
            "status": "success",
            "rows": len(final_df),
            "sample_output": final_df.head(10).to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ==============================
# WEEKLY FORECAST API
# ==============================
# @router.post("/forecast/weekly")
# def forecast_weekly(req: ForecastRequest):
#     try:
#         print(f"[API] Weekly request → {req}")

#         daily_df = fetch_day_aggregates(None, None)
#         if daily_df.empty:
#             raise Exception("No historical sales data found")

#         totals = (
#             daily_df.groupby(["site_code", "assortment_name"])["total_qty"]
#             .sum().reset_index()
#         )
#         top30 = (
#             totals.sort_values(["site_code", "total_qty"], ascending=[True, False])
#             .groupby("site_code").head(30)
#         )

#         filtered_df = daily_df.merge(
#             top30[["site_code", "assortment_name"]],
#             on=["site_code", "assortment_name"],
#             how="inner"
#         )

#         periods = req.horizon * 7
#         all_results = []

#         for (site, asmt), g in filtered_df.groupby(["site_code", "assortment_name"]):
#             sub_df = g[["day", "total_qty"]]
#             fc = forecast_one_assortment(sub_df, periods)

#             fc["site_code"] = site
#             fc["assortment_name"] = asmt

#             # Week start Monday
#             fc["prediction_date"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
#             fc["prediction_date"] = fc["prediction_date"].dt.date
#             fc["prediction_type"] = "weekly"

#             weekly_fc = fc.groupby(
#                 ["site_code", "assortment_name", "prediction_date", "prediction_type"],
#                 as_index=False
#             )["predicted_qty"].sum()

#             all_results.append(weekly_fc)

#         final_df = pd.concat(all_results, ignore_index=True)

#         start = pd.to_datetime(req.start_date).date()
#         end = pd.to_datetime(req.end_date).date()

#         final_df = final_df[
#             (final_df["prediction_date"] >= start) &
#             (final_df["prediction_date"] <= end)
#         ]

#         write_forecast_to_db(final_df, "weekly")

#         return {
#             "status": "success",
#             "rows": len(final_df),
#             "sample_output": final_df.head(10).to_dict(orient="records")
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/forecast/weekly")
def forecast_weekly(req: ForecastRequest):
    try:
        print(f"[API] Weekly request → {req}")

        # Load recent sales (limit inside ingest)
        daily_df = fetch_day_aggregates(None, None)
        if daily_df.empty:
            raise Exception("No historical sales data found")

        periods = req.horizon * 5  # Reduced horizon (stability improvement)
        all_results = []

        # Forecast each assortment separately
        for (site, asmt), g in daily_df.groupby(["site_code", "assortment_name"]):

            sub_df = g[["day", "total_qty"]]
            if len(sub_df) < 7:
                continue

            fc = forecast_one_assortment(sub_df, periods)

            fc["site_code"] = site
            fc["assortment_name"] = asmt

            # Convert to weekly forecast (week start Monday)
            fc["prediction_date"] = fc["day"] - pd.to_timedelta(fc["day"].dt.weekday, unit="D")
            fc["prediction_date"] = fc["prediction_date"].dt.date
            fc["prediction_type"] = "weekly"

            all_results.append(fc)

        if not all_results:
            raise Exception("No weekly forecast generated")

        final_df = pd.concat(all_results, ignore_index=True)

        # Aggregate by week and assortment
        final_df = (
            final_df.groupby(
                ["site_code", "assortment_name", "prediction_date", "prediction_type"],
                as_index=False
            )["predicted_qty"].sum()
        )

        # Filter within requested output date range
        start = pd.to_datetime(req.start_date).date()
        end = pd.to_datetime(req.end_date).date()
        final_df = final_df[
            (final_df["prediction_date"] >= start) &
            (final_df["prediction_date"] <= end)
        ]

        write_forecast_to_db(final_df, "weekly")

        return {
            "status": "success",
            "rows": len(final_df),
            "sample_output": final_df.head(10).to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Add routes
app.include_router(router)

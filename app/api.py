from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
from datetime import datetime
from app.ingest import fetch_day_aggregates
from app.forecast import forecast_one_assortment
from app.writer import write_forecast_to_db

app = FastAPI(title="Assortment Forecast API")
router = APIRouter()


# REQUEST MODEL
class ForecastRequest(BaseModel):
    start_date: str
    end_date: str
    horizon: int = 3


# MONTHLY FORECAST API
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



# WEEKLY FORECAST API
@router.post("/forecast/weekly")
def forecast_weekly(req: ForecastRequest):
    try:
        print(f"[API] Weekly request → {req}")

        daily_df = fetch_day_aggregates(None, None)
        if daily_df.empty:
            raise Exception("No historical sales data found")

        periods = req.horizon * 5  
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

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import requests
import time

# ---------------------
# Trigger Monthly API
# ---------------------
def trigger_monthly_forecast(horizon_months=3):
    payload = {
        "horizon": horizon_months,
        "method": "auto"        # new param for ML model selection
    }

    try:
        resp = requests.post(
            "http://localhost:8000/forecast/monthly",
            json=payload
        )
        print("Monthly triggered:", resp.status_code, resp.text)
    except Exception as e:
        print("Monthly trigger failed:", e)


# ---------------------
# Trigger Weekly API
# ---------------------
def trigger_weekly_forecast(horizon_weeks=4):
    payload = {
        "horizon": horizon_weeks,
        "method": "auto"        # new param for ML model
    }

    try:
        resp = requests.post(
            "http://localhost:8000/forecast/weekly",
            json=payload
        )
        print("Weekly triggered:", resp.status_code, resp.text)
    except Exception as e:
        print("Weekly trigger failed:", e)


# ---------------------
# Scheduler Start
# ---------------------
def start_scheduler():
    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    # Monthly Forecast → run 1st day of month at 02:00 AM
    scheduler.add_job(
        trigger_monthly_forecast,
        "cron",
        day=1,
        hour=2,
        minute=0,
        args=[3]
    )

    # Weekly Forecast → run every Monday at 03:00 AM
    scheduler.add_job(
        trigger_weekly_forecast,
        "cron",
        day_of_week="mon",
        hour=3,
        minute=0,
        args=[4]
    )

    scheduler.start()
    print("Scheduler started...")


# ---------------------
# Keep alive
# ---------------------
if __name__ == "__main__":
    start_scheduler()
    while True:
        time.sleep(60)

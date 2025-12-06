from pydantic import BaseModel

class ForecastRequest(BaseModel):
    horizon: int                      # monthly / weekly forecast horizon
    method: str = "auto"              # "auto", "xgboost", "lightgbm"
    start_date: str | None = None     # optional historical window
    end_date: str | None = None

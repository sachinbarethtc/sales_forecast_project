from pydantic import BaseModel

class ForecastRequest(BaseModel):
    horizon: int                     
    method: str = "auto"              
    start_date: str | None = None     
    end_date: str | None = None

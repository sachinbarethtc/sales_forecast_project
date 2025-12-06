# app/forecast.py

import pandas as pd
import numpy as np
from datetime import timedelta
from sklearn.metrics import mean_squared_error
from app.logger import logger

# =====================================================
# FEATURE ENGINEERING
# =====================================================
def create_features(df):
    df = df.copy()
    df["day"] = pd.to_datetime(df["day"])
    df = df.sort_values("day").set_index("day")

    df["lag_1"] = df["total_qty"].shift(1)
    df["lag_7"] = df["total_qty"].shift(7)
    df["lag_30"] = df["total_qty"].shift(30)

    df["roll_7"] = df["total_qty"].shift(1).rolling(7).mean()
    df["roll_30"] = df["total_qty"].shift(1).rolling(30).mean()

    df["dow"] = df.index.dayofweek
    df["month"] = df.index.month

    df = df.dropna()
    return df


# =====================================================
# TRAIN MODELS (LGB & XGB)
# =====================================================
def train_model(df, model_type="lgb"):
    from lightgbm import LGBMRegressor
    from xgboost import XGBRegressor

    X = df.drop(columns=["total_qty"])
    y = df["total_qty"]

    if model_type == "xgb":
        model = XGBRegressor(
            n_estimators=350,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            verbosity=0
        )
    else:
        model = LGBMRegressor(
            n_estimators=350,
            learning_rate=0.05,
        )

    model.fit(X, y)
    pred = model.predict(X)
    rmse = np.sqrt(mean_squared_error(y, pred))

    return model, rmse


# =====================================================
# FUTURE FORECAST (DAY WISE)
# =====================================================
def forecast_with_model(history_df, horizon_days, model):
    df = create_features(history_df)

    future_dates = []
    predictions = []

    qty_series = history_df["total_qty"].values.copy()
    last_date = pd.to_datetime(history_df["day"].max())

    for _ in range(horizon_days):
        next_day = last_date + timedelta(days=1)
        future_dates.append(next_day)

        lag_1 = qty_series[-1]
        lag_7 = np.mean(qty_series[-7:]) if len(qty_series) >= 7 else lag_1
        lag_30 = np.mean(qty_series[-30:]) if len(qty_series) >= 30 else lag_7

        roll_7 = lag_7
        roll_30 = lag_30

        dow = next_day.dayofweek
        month = next_day.month

        row = np.array([
            lag_1, lag_7, lag_30, roll_7, roll_30, dow, month
        ]).reshape(1, -1)

        yhat = float(model.predict(row)[0])
        predictions.append(yhat)

        qty_series = np.append(qty_series, yhat)
        last_date = next_day

    return pd.DataFrame({
        "day": future_dates,
        "predicted_qty": predictions
    })


# =====================================================
# MAIN API FUNCTION
# =====================================================
def forecast_one_assortment(df_daily, horizon_days):
    """
    df_daily → columns: [day, total_qty]
    returns → dataframe: [day, predicted_qty]
    """

    df = df_daily.copy()
    df["day"] = pd.to_datetime(df["day"])
    df = df.sort_values("day")

    # -------------------------------------------------
    # FALLBACK: not enough data
    # -------------------------------------------------
    if df.shape[0] < 40:
        logger.warning(f"[FORECAST] Fallback (Not enough data: {df.shape[0]} rows)")
        avg_qty = float(df["total_qty"].mean()) if df.shape[0] else 0.0

        future_dates = pd.date_range(
            df["day"].max() + timedelta(days=1),
            periods=horizon_days
        )

        return pd.DataFrame({
            "day": future_dates,
            "predicted_qty": [avg_qty] * horizon_days
        })

    # Build features
    feat = create_features(df)
    if feat.empty:
        avg_qty = float(df["total_qty"].mean())
        future_dates = pd.date_range(df["day"].max() + timedelta(days=1),
                                     periods=horizon_days)
        return pd.DataFrame({
            "day": future_dates,
            "predicted_qty": [avg_qty] * horizon_days
        })

    # Train two models
    try:
        model_lgb, rmse_lgb = train_model(feat, "lgb")
        model_xgb, rmse_xgb = train_model(feat, "xgb")

        model = model_lgb if rmse_lgb <= rmse_xgb else model_xgb

        logger.info(
            f"[MODEL] Selected: {'LGBM' if model is model_lgb else 'XGB'} "
            f"(lgb={rmse_lgb:.3f}, xgb={rmse_xgb:.3f})"
        )

        return forecast_with_model(df, horizon_days, model)

    except Exception:
        logger.exception("[FORECAST] Model failed — fallback")
        avg_qty = float(df["total_qty"].mean())
        future_dates = pd.date_range(df["day"].max() + timedelta(days=1),
                                     periods=horizon_days)
        return pd.DataFrame({
            "day": future_dates,
            "predicted_qty": [avg_qty] * horizon_days
        })

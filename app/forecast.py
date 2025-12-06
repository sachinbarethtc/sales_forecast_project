# # # # import pandas as pd
# # # # import numpy as np
# # # # from datetime import timedelta

# # # # from xgboost import XGBRegressor
# # # # from lightgbm import LGBMRegressor
# # # # from statsmodels.tsa.arima.model import ARIMA


# # # # # --------------------
# # # # # FEATURE ENGINEERING
# # # # # --------------------
# # # # def create_features(df):
# # # #     df = df.copy()
# # # #     df["day"] = pd.to_datetime(df["day"])
# # # #     df = df.set_index("day")

# # # #     df["lag_1"] = df["total_qty"].shift(1)
# # # #     df["lag_7"] = df["total_qty"].shift(7)
# # # #     df["lag_30"] = df["total_qty"].shift(30)

# # # #     df["roll_mean_7"] = df["total_qty"].shift(1).rolling(7).mean()
# # # #     df["roll_mean_30"] = df["total_qty"].shift(1).rolling(30).mean()

# # # #     df["dow"] = df.index.dayofweek
# # # #     df["month"] = df.index.month

# # # #     df = df.dropna()
# # # #     return df


# # # # # ------------------------
# # # # # TRAIN ML MODEL
# # # # # ------------------------
# # # # def train_ml_model(df, model_type="xgboost"):
# # # #     X = df.drop("total_qty", axis=1)
# # # #     y = df["total_qty"]

# # # #     if model_type == "xgboost":
# # # #         model = XGBRegressor(
# # # #             n_estimators=300,
# # # #             learning_rate=0.05,
# # # #             max_depth=6,
# # # #             subsample=0.8,
# # # #             colsample_bytree=0.8,
# # # #             objective="reg:squarederror"
# # # #         )
# # # #     else:
# # # #         model = LGBMRegressor(
# # # #             n_estimators=300,
# # # #             learning_rate=0.05,
# # # #             max_depth=-1
# # # #         )

# # # #     model.fit(X, y)
# # # #     return model


# # # # # ------------------------
# # # # # ML FORECASTING
# # # # # ------------------------
# # # # def forecast_ml(df, horizon_days=30, model_type="xgboost"):
# # # #     df = df.copy()
# # # #     df = create_features(df)

# # # #     model = train_ml_model(df, model_type)

# # # #     future_dates = []
# # # #     preds = []

# # # #     last_date = df.index[-1]
# # # #     last_row = df.iloc[-1].copy()

# # # #     for i in range(horizon_days):
# # # #         next_date = last_date + timedelta(days=1)
# # # #         future_dates.append(next_date)

# # # #         next_row = last_row.copy()
# # # #         next_row["lag_1"] = last_row["total_qty"]
# # # #         next_row["lag_7"] = df["total_qty"].iloc[-7:].mean()
# # # #         next_row["lag_30"] = df["total_qty"].iloc[-30:].mean()
# # # #         next_row["roll_mean_7"] = df["total_qty"].iloc[-7:].mean()
# # # #         next_row["roll_mean_30"] = df["total_qty"].iloc[-30:].mean()

# # # #         next_row["dow"] = next_date.dayofweek
# # # #         next_row["month"] = next_date.month

# # # #         X_pred = next_row.drop(labels=["total_qty"], errors="ignore").values.reshape(1, -1)
# # # #         y_pred = model.predict(X_pred)[0]

# # # #         preds.append(y_pred)

# # # #         new_row = pd.DataFrame({"total_qty": y_pred}, index=[next_date])
# # # #         df = pd.concat([df, new_row])

# # # #         last_row = next_row.copy()
# # # #         last_row["total_qty"] = y_pred
# # # #         last_date = next_date

# # # #     preds = np.array(preds)
# # # #     std = preds.std()

# # # #     res = pd.DataFrame({
# # # #         "day": future_dates,
# # # #         "yhat": preds,
# # # #         "yhat_lower": preds - std,
# # # #         "yhat_upper": preds + std
# # # #     })
# # # #     return res


# # # # # ------------------------
# # # # # ARIMA FALLBACK
# # # # # ------------------------
# # # # def forecast_arima(df, horizon_days=30):
# # # #     df = df.copy()
# # # #     df = df.set_index("day")["total_qty"].asfreq("D").fillna(0)

# # # #     model = ARIMA(df, order=(1, 1, 1))
# # # #     fit = model.fit()

# # # #     pred = fit.get_forecast(steps=horizon_days)
# # # #     ci = pred.conf_int()

# # # #     future_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=horizon_days)

# # # #     res = pd.DataFrame({
# # # #         "day": future_dates,
# # # #         "yhat": pred.predicted_mean.values,
# # # #         "yhat_lower": ci.iloc[:, 0].values,
# # # #         "yhat_upper": ci.iloc[:, 1].values
# # # #     })
# # # #     return res


# # # # # ------------------------
# # # # # AUTO-MODEL SELECTOR
# # # # # ------------------------
# # # # def forecast(df, horizon_days=30, method="xgboost"):
# # # #     try:
# # # #         return forecast_ml(df, horizon_days, method)
# # # #     except:
# # # #         return forecast_arima(df, horizon_days)


# # # import pandas as pd
# # # import numpy as np
# # # from datetime import timedelta
# # # from sklearn.metrics import mean_squared_error

# # # from xgboost import XGBRegressor
# # # from lightgbm import LGBMRegressor
# # # from statsmodels.tsa.arima.model import ARIMA


# # # # -----------------------------
# # # # CREATE FEATURES
# # # # -----------------------------
# # # def create_features(df):
# # #     df = df.copy()
# # #     df["day"] = pd.to_datetime(df["day"])
# # #     df = df.set_index("day")

# # #     df["lag_1"] = df["total_qty"].shift(1)
# # #     df["lag_7"] = df["total_qty"].shift(7)
# # #     df["lag_30"] = df["total_qty"].shift(30)

# # #     df["roll_mean_7"] = df["total_qty"].shift(1).rolling(7).mean()
# # #     df["roll_mean_30"] = df["total_qty"].shift(1).rolling(30).mean()

# # #     df["dow"] = df.index.dayofweek
# # #     df["month"] = df.index.month

# # #     df = df.dropna()
# # #     return df


# # # # -----------------------------
# # # # TRAIN MODEL
# # # # -----------------------------
# # # def train_model(df, model_type):
# # #     X = df.drop("total_qty", axis=1)
# # #     y = df["total_qty"]

# # #     if model_type == "xgboost":
# # #         model = XGBRegressor(
# # #             n_estimators=300,
# # #             learning_rate=0.05,
# # #             max_depth=6,
# # #             subsample=0.8,
# # #             colsample_bytree=0.8,
# # #             objective="reg:squarederror"
# # #         )
# # #     else:
# # #         model = LGBMRegressor(
# # #             n_estimators=300,
# # #             learning_rate=0.05
# # #         )

# # #     model.fit(X, y)
# # #     preds = model.predict(X)
# # #     rmse = np.sqrt(mean_squared_error(y, preds))

# # #     return model, rmse


# # # # -----------------------------
# # # # FORECAST USING ML MODEL
# # # # -----------------------------
# # # def forecast_with_model(df, horizon_days, model):
# # #     df = df.copy()
# # #     df = create_features(df)

# # #     future_dates = []
# # #     preds = []

# # #     last_date = df.index[-1]
# # #     last_row = df.iloc[-1].copy()

# # #     for i in range(horizon_days):
# # #         next_date = last_date + timedelta(days=1)
# # #         future_dates.append(next_date)

# # #         next_row = last_row.copy()
# # #         next_row["lag_1"] = last_row["total_qty"]
# # #         next_row["lag_7"] = df["total_qty"].iloc[-7:].mean()
# # #         next_row["lag_30"] = df["total_qty"].iloc[-30:].mean()

# # #         next_row["roll_mean_7"] = df["total_qty"].iloc[-7:].mean()
# # #         next_row["roll_mean_30"] = df["total_qty"].iloc[-30:].mean()

# # #         next_row["dow"] = next_date.dayofweek
# # #         next_row["month"] = next_date.month

# # #         X_pred = next_row.drop(labels=["total_qty"], errors="ignore").values.reshape(1, -1)
# # #         y_pred = model.predict(X_pred)[0]

# # #         preds.append(y_pred)

# # #         new_row = pd.DataFrame({"total_qty": y_pred}, index=[next_date])
# # #         df = pd.concat([df, new_row])

# # #         last_row = next_row.copy()
# # #         last_row["total_qty"] = y_pred
# # #         last_date = next_date

# # #     preds = np.array(preds)
# # #     std = preds.std()

# # #     return pd.DataFrame({
# # #         "day": future_dates,
# # #         "yhat": preds,
# # #         "yhat_lower": preds - std,
# # #         "yhat_upper": preds + std
# # #     })


# # # # -----------------------------
# # # # AUTO MODEL SELECT
# # # # -----------------------------
# # # def forecast(df, horizon_days=30):
# # #     df_features = create_features(df)

# # #     # Train both models
# # #     model_xgb, rmse_xgb = train_model(df_features, "xgboost")
# # #     model_lgb, rmse_lgb = train_model(df_features, "lightgbm")

# # #     # Pick best model based on RMSE
# # #     best_model = model_lgb if rmse_lgb < rmse_xgb else model_xgb

# # #     # Forecast using the best model
# # #     return forecast_with_model(df, horizon_days, best_model)




# # import pandas as pd
# # import numpy as np
# # from datetime import timedelta
# # from sklearn.metrics import mean_squared_error


# # # -----------------------------
# # # CREATE FEATURES
# # # -----------------------------
# # def create_features(df):
# #     df = df.copy()
# #     df["day"] = pd.to_datetime(df["day"])
# #     df = df.set_index("day")

# #     df["lag_1"] = df["total_qty"].shift(1)
# #     df["lag_7"] = df["total_qty"].shift(7)
# #     df["lag_30"] = df["total_qty"].shift(30)

# #     df["roll_mean_7"] = df["total_qty"].shift(1).rolling(7).mean()
# #     df["roll_mean_30"] = df["total_qty"].shift(1).rolling(30).mean()

# #     df["dow"] = df.index.dayofweek
# #     df["month"] = df.index.month

# #     df = df.dropna()
# #     return df


# # # -----------------------------
# # # TRAIN MODEL (LAZY IMPORT)
# # # -----------------------------
# # def train_model(df, model_type):
# #     # lazy import to avoid Swagger freezing
# #     from xgboost import XGBRegressor
# #     from lightgbm import LGBMRegressor

# #     X = df.drop("total_qty", axis=1)
# #     y = df["total_qty"]

# #     if model_type == "xgboost":
# #         model = XGBRegressor(
# #             n_estimators=300,
# #             learning_rate=0.05,
# #             max_depth=6,
# #             subsample=0.8,
# #             colsample_bytree=0.8,
# #             objective="reg:squarederror"
# #         )
# #     else:
# #         model = LGBMRegressor(
# #             n_estimators=300,
# #             learning_rate=0.05
# #         )

# #     model.fit(X, y)
# #     preds = model.predict(X)
# #     rmse = np.sqrt(mean_squared_error(y, preds))

# #     return model, rmse


# # # -----------------------------
# # # FORECAST USING MODEL
# # # -----------------------------
# # def forecast_with_model(df, horizon_days, model):
# #     df = df.copy()
# #     df = create_features(df)

# #     future_dates = []
# #     preds = []

# #     last_date = df.index[-1]
# #     last_row = df.iloc[-1].copy()

# #     for i in range(horizon_days):
# #         next_date = last_date + timedelta(days=1)
# #         future_dates.append(next_date)

# #         next_row = last_row.copy()
# #         next_row["lag_1"] = last_row["total_qty"]
# #         next_row["lag_7"] = df["total_qty"].iloc[-7:].mean()
# #         next_row["lag_30"] = df["total_qty"].iloc[-30:].mean()

# #         next_row["roll_mean_7"] = df["total_qty"].iloc[-7:].mean()
# #         next_row["roll_mean_30"] = df["total_qty"].iloc[-30:].mean()

# #         next_row["dow"] = next_date.dayofweek
# #         next_row["month"] = next_date.month

# #         X_pred = next_row.drop(labels=["total_qty"], errors="ignore").values.reshape(1, -1)
# #         y_pred = model.predict(X_pred)[0]

# #         preds.append(y_pred)

# #         new_row = pd.DataFrame({"total_qty": y_pred}, index=[next_date])
# #         df = pd.concat([df, new_row])

# #         last_row = next_row.copy()
# #         last_row["total_qty"] = y_pred
# #         last_date = next_date

# #     preds = np.array(preds)
# #     std = preds.std()

# #     return pd.DataFrame({
# #         "day": future_dates,
# #         "yhat": preds,
# #         "yhat_lower": preds - std,
# #         "yhat_upper": preds + std
# #     })


# # # -----------------------------
# # # ARIMA FALLBACK (LAZY IMPORT)
# # # -----------------------------
# # def forecast_arima(df, horizon_days):
# #     from statsmodels.tsa.arima.model import ARIMA       # <--- lazy import

# #     df = df.copy()
# #     df = df.set_index("day")["total_qty"].asfreq("D").fillna(0)

# #     model = ARIMA(df, order=(1, 1, 1))
# #     fit = model.fit()

# #     pred = fit.get_forecast(steps=horizon_days)
# #     ci = pred.conf_int()

# #     future_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=horizon_days)

# #     return pd.DataFrame({
# #         "day": future_dates,
# #         "yhat": pred.predicted_mean.values,
# #         "yhat_lower": ci.iloc[:, 0].values,
# #         "yhat_upper": ci.iloc[:, 1].values
# #     })


# # # -----------------------------
# # # AUTO MODEL SELECT
# # # -----------------------------
# # def forecast(df, horizon_days=30):
# #     df_features = create_features(df)

# #     # Train both models
# #     model_xgb, rmse_xgb = train_model(df_features, "xgboost")
# #     model_lgb, rmse_lgb = train_model(df_features, "lightgbm")

# #     # Pick best model based on RMSE
# #     best_model = model_lgb if rmse_lgb < rmse_xgb else model_xgb

# #     # Forecast using the best model
# #     return forecast_with_model(df, horizon_days, best_model)


# import pandas as pd
# import numpy as np
# from datetime import timedelta
# from sklearn.metrics import mean_squared_error


# def create_features(df):
#     df = df.copy()
#     df["day"] = pd.to_datetime(df["day"])
#     df = df.set_index("day")

#     df["lag_1"] = df["total_qty"].shift(1)
#     df["lag_7"] = df["total_qty"].shift(7)
#     df["lag_30"] = df["total_qty"].shift(30)

#     df["roll_mean_7"] = df["total_qty"].shift(1).rolling(7).mean()
#     df["roll_mean_30"] = df["total_qty"].shift(1).rolling(30).mean()

#     df["dow"] = df.index.dayofweek
#     df["month"] = df.index.month

#     df = df.dropna()
#     return df


# def train_model(df, model_type):
#     # Lazy imports
#     from xgboost import XGBRegressor
#     from lightgbm import LGBMRegressor

#     X = df.drop("total_qty", axis=1)
#     y = df["total_qty"]

#     if model_type == "xgboost":
#         model = XGBRegressor(
#             n_estimators=300,
#             learning_rate=0.05,
#             max_depth=6,
#             subsample=0.8,
#             colsample_bytree=0.8,
#             objective="reg:squarederror"
#         )
#     else:
#         model = LGBMRegressor(
#             n_estimators=300,
#             learning_rate=0.05
#         )

#     model.fit(X, y)
#     preds = model.predict(X)
#     rmse = np.sqrt(mean_squared_error(y, preds))

#     return model, rmse


# def forecast_with_model(df, horizon_days, model):
#     df = df.copy()
#     df = create_features(df)

#     future_dates = []
#     preds = []

#     last_date = df.index[-1]
#     last_row = df.iloc[-1].copy()

#     for _ in range(horizon_days):
#         next_date = last_date + timedelta(days=1)
#         future_dates.append(next_date)

#         next_row = last_row.copy()
#         next_row["lag_1"] = last_row["total_qty"]
#         next_row["lag_7"] = df["total_qty"].iloc[-7:].mean()
#         next_row["lag_30"] = df["total_qty"].iloc[-30:].mean()

#         next_row["roll_mean_7"] = df["total_qty"].iloc[-7:].mean()
#         next_row["roll_mean_30"] = df["total_qty"].iloc[-30:].mean()

#         next_row["dow"] = next_date.dayofweek
#         next_row["month"] = next_date.month

#         X_pred = next_row.drop(labels=["total_qty"], errors="ignore").values.reshape(1, -1)
#         y_pred = model.predict(X_pred)[0]

#         preds.append(y_pred)

#         new_row = pd.DataFrame({"total_qty": y_pred}, index=[next_date])
#         df = pd.concat([df, new_row])

#         last_row = next_row.copy()
#         last_row["total_qty"] = y_pred
#         last_date = next_date

#     preds = np.array(preds)
#     std = preds.std()

#     return pd.DataFrame({
#         "day": future_dates,
#         "yhat": preds,
#         "yhat_lower": preds - std,
#         "yhat_upper": preds + std
#     })


# def forecast(df, horizon_days=30):
#     df_features = create_features(df)

#     # Train both models
#     model_xgb, rmse_xgb = train_model(df_features, "xgboost")
#     model_lgb, rmse_lgb = train_model(df_features, "lightgbm")

#     best = model_lgb if rmse_lgb < rmse_xgb else model_xgb
#     return forecast_with_model(df, horizon_days, best)



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

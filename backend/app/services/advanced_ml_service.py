import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from app.models.fx_models import ExchangeRate, ForecastResult, ModelMetric

class AdvancedForecastService:
    def __init__(self, db: Session):
        self.db = db

    def _df(self, pair: str):
        rows = self.db.query(ExchangeRate).filter(ExchangeRate.pair == pair).order_by(ExchangeRate.captured_at.asc()).limit(800).all()
        return pd.DataFrame([{
            "bid": r.bid,
            "high": r.high or r.bid,
            "low": r.low or r.bid,
            "pct_change": r.pct_change or 0
        } for r in rows])

    def _prepare(self, df):
        df = df.copy()
        df["t"] = np.arange(len(df))
        df["ret"] = df["bid"].pct_change().fillna(0)
        df["ma3"] = df["bid"].rolling(3).mean().bfill()
        df["ma5"] = df["bid"].rolling(5).mean().bfill()
        df["vol3"] = df["ret"].rolling(3).std().fillna(0)
        df["vol5"] = df["ret"].rolling(5).std().fillna(0)
        df["range_pct"] = ((df["high"] - df["low"]) / df["bid"]).replace([np.inf, -np.inf], 0).fillna(0)
        df["target"] = df["bid"].shift(-1)
        df = df.dropna()
        X = df[["t", "bid", "ret", "ma3", "ma5", "vol3", "vol5", "range_pct"]]
        y = df["target"]
        return df, X, y

    def forecast_pair(self, pair: str):
        raw = self._df(pair)
        if len(raw) < 6:
            current = float(raw["bid"].iloc[-1]) if len(raw) else 0.0
            f = ForecastResult(
                pair=pair,
                current_value=current,
                predicted_value=current,
                expected_change_pct=0,
                confidence=0.10,
                risk_level="unknown",
                model_name="fallback_insufficient_data",
                technical_summary="Poucos dados. Execute a coleta mais vezes ou importe histórico."
            )
            self.db.add(f)
            self.db.commit()
            return self._out(f)

        df, X, y = self._prepare(raw)
        split = max(3, int(len(X) * 0.75))
        X_train, X_test = X.iloc[:split], X.iloc[split:]
        y_train, y_test = y.iloc[:split], y.iloc[split:]

        models = [
            ("linear_regression", LinearRegression()),
            ("random_forest", RandomForestRegressor(n_estimators=80, random_state=42)),
            ("gradient_boosting", GradientBoostingRegressor(random_state=42)),
        ]

        latest = X.iloc[[-1]].copy()
        latest["t"] = float(latest["t"].iloc[0]) + 7
        predictions = []
        mapes = []

        for name, model in models:
            model.fit(X_train, y_train)
            if len(X_test):
                pred_test = model.predict(X_test)
                mae = float(mean_absolute_error(y_test, pred_test))
                mape = float(mean_absolute_percentage_error(y_test, pred_test))
            else:
                mae, mape = 0.0, 1.0

            predictions.append(float(model.predict(latest)[0]))
            mapes.append(mape)
            self.db.add(ModelMetric(pair=pair, model_name=name, mae=mae, mape=mape, samples=len(X)))

        current = float(raw["bid"].iloc[-1])
        predicted = float(np.mean(predictions))
        change_pct = ((predicted - current) / current * 100) if current else 0
        confidence = max(0.15, min(0.92, 1 - float(np.mean(mapes))))
        vol = float(df["vol5"].iloc[-1])

        if abs(change_pct) > 3 or vol > 0.03:
            risk = "high"
        elif abs(change_pct) > 1 or vol > 0.012:
            risk = "medium"
        else:
            risk = "low"

        summary = f"Ensemble ML com {len(X)} amostras. Mudança esperada {change_pct:.2f}%. Volatilidade {vol:.4f}. Risco {risk}."

        f = ForecastResult(
            pair=pair,
            current_value=current,
            predicted_value=predicted,
            expected_change_pct=change_pct,
            confidence=confidence,
            risk_level=risk,
            model_name="ensemble_lr_rf_gb",
            technical_summary=summary
        )
        self.db.add(f)
        self.db.commit()
        return self._out(f)

    def forecast_all(self):
        pairs = [x[0] for x in self.db.query(ExchangeRate.pair).distinct().all()]
        return [self.forecast_pair(pair) for pair in pairs]

    def _out(self, f):
        return {
            "pair": f.pair,
            "current_value": round(f.current_value, 6),
            "predicted_value": round(f.predicted_value, 6),
            "expected_change_pct": round(f.expected_change_pct, 3),
            "confidence": round(f.confidence, 3),
            "risk_level": f.risk_level,
            "model_name": f.model_name,
            "technical_summary": f.technical_summary
        }

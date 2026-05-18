from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.db.session import Base

class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(20), index=True)
    base_currency = Column(String(10))
    quote_currency = Column(String(10))
    bid = Column(Float)
    ask = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    pct_change = Column(Float, nullable=True)
    source = Column(String(80))
    reliability = Column(String(60))
    source_note = Column(Text, nullable=True)
    captured_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

class ForecastResult(Base):
    __tablename__ = "forecast_results"
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(20), index=True)
    current_value = Column(Float)
    predicted_value = Column(Float)
    expected_change_pct = Column(Float)
    confidence = Column(Float)
    risk_level = Column(String(40))
    model_name = Column(String(120))
    technical_summary = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(20), index=True)
    action = Column(String(60))
    score = Column(Float)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelMetric(Base):
    __tablename__ = "model_metrics"
    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(20), index=True)
    model_name = Column(String(120))
    mae = Column(Float)
    mape = Column(Float)
    samples = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AlertLog(Base):
    __tablename__ = "alert_logs"
    id = Column(Integer, primary_key=True, index=True)
    channel = Column(String(40))
    target = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=True)
    message = Column(Text)
    attachment_path = Column(String(500), nullable=True)
    success = Column(Boolean, default=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AgentRun(Base):
    __tablename__ = "agent_runs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120))
    status = Column(String(40))
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

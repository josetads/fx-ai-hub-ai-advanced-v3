from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.fx_models import ExchangeRate, ForecastResult, Recommendation, ModelMetric, AlertLog
from app.services.currency_collector import CurrencyCollectorService
from app.services.advanced_ml_service import AdvancedForecastService
from app.services.recommendation_service import RecommendationService
from app.services.report_service import ReportService
from app.agents.enterprise_agent import EnterpriseAgent

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok", "version": "V3"}

@router.get("/rates/collect")
def collect(db: Session = Depends(get_db)):
    return CurrencyCollectorService(db).collect_all()

@router.get("/rates/latest")
def latest(db: Session = Depends(get_db)):
    rows = db.query(ExchangeRate).order_by(ExchangeRate.captured_at.desc()).limit(100).all()
    return [{"pair": r.pair, "bid": r.bid, "source": r.source, "reliability": r.reliability, "captured_at": str(r.captured_at)} for r in rows]

@router.get("/ml/forecast/{pair}")
def forecast_pair(pair: str, db: Session = Depends(get_db)):
    return AdvancedForecastService(db).forecast_pair(pair.upper())

@router.get("/ml/forecast-all")
def forecast_all(db: Session = Depends(get_db)):
    return AdvancedForecastService(db).forecast_all()

@router.get("/recommendations/{pair}")
def rec_pair(pair: str, db: Session = Depends(get_db)):
    return RecommendationService(db).recommend_pair(pair.upper())

@router.get("/recommendations/all")
def rec_all(db: Session = Depends(get_db)):
    return RecommendationService(db).recommend_all()

@router.get("/reports/generate")
def report(db: Session = Depends(get_db)):
    return {"report_path": ReportService(db).generate()}

@router.post("/agents/run-enterprise-cycle")
def run_agent(db: Session = Depends(get_db)):
    return EnterpriseAgent(db).run()

@router.get("/erp/export-json")
def erp(db: Session = Depends(get_db)):
    rates = db.query(ExchangeRate).order_by(ExchangeRate.captured_at.desc()).limit(50).all()
    forecasts = db.query(ForecastResult).order_by(ForecastResult.created_at.desc()).limit(50).all()
    recs = db.query(Recommendation).order_by(Recommendation.created_at.desc()).limit(50).all()
    return {
        "target": "ERP_SMART_FACTORY",
        "rates": [{"pair": r.pair, "bid": r.bid, "captured_at": str(r.captured_at)} for r in rates],
        "forecasts": [{"pair": f.pair, "predicted": f.predicted_value, "change_pct": f.expected_change_pct, "risk": f.risk_level, "confidence": f.confidence} for f in forecasts],
        "recommendations": [{"pair": r.pair, "action": r.action, "score": r.score, "reason": r.reason} for r in recs]
    }

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    rows = db.query(ModelMetric).order_by(ModelMetric.created_at.desc()).limit(100).all()
    return [{"pair": m.pair, "model": m.model_name, "mae": m.mae, "mape": m.mape, "samples": m.samples} for m in rows]

@router.get("/logs/alerts")
def logs(db: Session = Depends(get_db)):
    rows = db.query(AlertLog).order_by(AlertLog.created_at.desc()).limit(100).all()
    return [{"channel": l.channel, "success": l.success, "error": l.error, "attachment": l.attachment_path, "created_at": str(l.created_at)} for l in rows]

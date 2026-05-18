from pathlib import Path
from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.fx_models import ExchangeRate, ForecastResult, Recommendation, ModelMetric, AlertLog

class ReportService:
    def __init__(self, db: Session):
        self.db = db
        Path(settings.REPORTS_DIR).mkdir(exist_ok=True)

    def generate(self):
        path = Path(settings.REPORTS_DIR) / f"fx_ai_hub_v3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        rates = self.db.query(ExchangeRate).order_by(ExchangeRate.captured_at.desc()).limit(1000).all()
        forecasts = self.db.query(ForecastResult).order_by(ForecastResult.created_at.desc()).limit(300).all()
        recs = self.db.query(Recommendation).order_by(Recommendation.created_at.desc()).limit(300).all()
        metrics = self.db.query(ModelMetric).order_by(ModelMetric.created_at.desc()).limit(300).all()
        logs = self.db.query(AlertLog).order_by(AlertLog.created_at.desc()).limit(100).all()

        dfs = {
            "Resumo Executivo": pd.DataFrame([
                {"Indicador": "Produto", "Valor": "FX AI Hub AI Advanced V3"},
                {"Indicador": "Finalidade", "Valor": "Previsão cambial e recomendação de compra para indústria."},
                {"Indicador": "Integração", "Valor": "ERP/Smart Factory via API REST."},
                {"Indicador": "IA", "Valor": "Ensemble ML + agentes + estrutura para LLM/RAG."}
            ]),
            "Cotacoes": pd.DataFrame([r.__dict__ for r in rates]).drop(columns=["_sa_instance_state"], errors="ignore"),
            "Previsoes IA": pd.DataFrame([f.__dict__ for f in forecasts]).drop(columns=["_sa_instance_state"], errors="ignore"),
            "Recomendacoes": pd.DataFrame([r.__dict__ for r in recs]).drop(columns=["_sa_instance_state"], errors="ignore"),
            "Metricas Modelo": pd.DataFrame([m.__dict__ for m in metrics]).drop(columns=["_sa_instance_state"], errors="ignore"),
            "Logs Alertas": pd.DataFrame([l.__dict__ for l in logs]).drop(columns=["_sa_instance_state"], errors="ignore"),
        }

        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            for name, df in dfs.items():
                df.to_excel(writer, index=False, sheet_name=name[:31])
            for sheet in writer.book.worksheets:
                for col in sheet.columns:
                    width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                    sheet.column_dimensions[col[0].column_letter].width = min(width + 3, 70)

        return str(path)

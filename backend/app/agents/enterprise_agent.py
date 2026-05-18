from sqlalchemy.orm import Session
from app.models.fx_models import AgentRun
from app.services.currency_collector import CurrencyCollectorService
from app.services.advanced_ml_service import AdvancedForecastService
from app.services.recommendation_service import RecommendationService
from app.services.report_service import ReportService
from app.services.email_service import EmailService
from app.services.telegram_service import TelegramService

class EnterpriseAgent:
    def __init__(self, db: Session):
        self.db = db

    def run(self):
        steps = []
        rates = CurrencyCollectorService(self.db).collect_all()
        steps.append({"agent": "collector", "items": len(rates)})

        forecasts = AdvancedForecastService(self.db).forecast_all()
        steps.append({"agent": "advanced_ml", "items": len(forecasts)})

        recs = RecommendationService(self.db).recommend_all()
        steps.append({"agent": "recommender", "items": len(recs)})

        report = ReportService(self.db).generate()
        steps.append({"agent": "report", "file": report})

        summary = "FX AI Hub AI Advanced: relatório gerado com cotações, previsões, métricas e recomendações."
        email = EmailService(self.db).send_report("FX AI Hub V3 - Relatório Cambial IA", summary, report)
        telegram = TelegramService(self.db).send_report(summary, report)

        steps.append({"agent": "email", "result": email})
        steps.append({"agent": "telegram", "result": telegram})

        self.db.add(AgentRun(name="enterprise_cycle", status="completed", details=str(steps)))
        self.db.commit()

        return {"status": "completed", "steps": steps, "report_path": report}

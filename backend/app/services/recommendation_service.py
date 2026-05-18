from sqlalchemy.orm import Session
from app.models.fx_models import ForecastResult, Recommendation

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def recommend_pair(self, pair: str):
        f = self.db.query(ForecastResult).filter(ForecastResult.pair == pair).order_by(ForecastResult.created_at.desc()).first()

        if not f:
            action, score, reason = "RODAR_PREVISAO", 0.20, "Execute a previsão antes da recomendação."
        elif pair == "KPW-BRL":
            action, score = "REFERENCIA_NAO_OPERACIONAL", 0.35
            reason = "KPW exige fonte alternativa/paga/manual auditada. Não usar como base única de compra."
        elif f.expected_change_pct > 1.5 and f.confidence >= 0.55:
            action, score = "COMPRAR_AGORA", min(0.95, 0.60 + f.confidence / 3)
            reason = f"Previsão indica alta de {f.expected_change_pct:.2f}%. Comprar agora pode reduzir custo."
        elif f.expected_change_pct < -1.0 and f.confidence >= 0.50:
            action, score = "AGUARDAR_QUEDA", min(0.90, 0.55 + f.confidence / 3)
            reason = f"Previsão indica queda de {abs(f.expected_change_pct):.2f}%. Aguardar pode ser melhor se houver estoque."
        elif f.risk_level == "high":
            action, score = "DIVIDIR_COMPRA", 0.72
            reason = "Risco alto. Recomenda-se compra fracionada."
        else:
            action, score = "MONITORAR", 0.58
            reason = "Sem sinal forte. Continuar monitorando."

        rec = Recommendation(pair=pair, action=action, score=score, reason=reason)
        self.db.add(rec)
        self.db.commit()
        return {"pair": pair, "action": action, "score": round(score, 3), "reason": reason}

    def recommend_all(self):
        pairs = [x[0] for x in self.db.query(ForecastResult.pair).distinct().all()]
        return [self.recommend_pair(pair) for pair in pairs]

import random
import requests
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.fx_models import ExchangeRate

class CurrencyCollectorService:
    def __init__(self, db: Session):
        self.db = db

    def collect_market(self):
        url = f"{settings.AWESOME_API_BASE}/json/last/{settings.DEFAULT_PAIRS}"
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        payload = res.json()
        saved = []

        for _, item in payload.items():
            base = item.get("code")
            quote = item.get("codein")
            r = ExchangeRate(
                pair=f"{base}-{quote}",
                base_currency=base,
                quote_currency=quote,
                bid=float(item.get("bid", 0)),
                ask=float(item.get("ask", 0)) if item.get("ask") else None,
                high=float(item.get("high", 0)) if item.get("high") else None,
                low=float(item.get("low", 0)) if item.get("low") else None,
                pct_change=float(item.get("pctChange", 0)) if item.get("pctChange") else None,
                source="awesomeapi",
                reliability="market_api",
                source_note="API pública de moedas."
            )
            self.db.add(r)
            saved.append(r)

        self.db.commit()
        return saved

    def collect_kpw(self):
        if not settings.KPW_ENABLED:
            return None
        value = max(0.0001, float(settings.KPW_MANUAL_BRL_VALUE) + random.uniform(-0.0001, 0.0001))
        r = ExchangeRate(
            pair="KPW-BRL",
            base_currency="KPW",
            quote_currency="BRL",
            bid=value,
            ask=value,
            high=value,
            low=value,
            pct_change=0.0,
            source="manual_or_alternative",
            reliability="low_liquidity_reference",
            source_note=settings.KPW_SOURCE_NOTE
        )
        self.db.add(r)
        self.db.commit()
        return r

    def collect_all(self):
        rates = self.collect_market()
        kpw = self.collect_kpw()
        if kpw:
            rates.append(kpw)
        return [{"pair": r.pair, "bid": r.bid, "source": r.source, "reliability": r.reliability} for r in rates]

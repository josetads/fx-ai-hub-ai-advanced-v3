from pathlib import Path
import requests
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.fx_models import AlertLog

class TelegramService:
    def __init__(self, db: Session):
        self.db = db

    def send_report(self, caption: str, attachment_path: str):
        if not settings.TELEGRAM_ENABLED:
            self._log("telegram", settings.TELEGRAM_CHAT_ID, None, caption, attachment_path, False, "Telegram disabled")
            return {"status": "disabled"}

        try:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendDocument"
            p = Path(attachment_path)
            with p.open("rb") as f:
                res = requests.post(url, data={"chat_id": settings.TELEGRAM_CHAT_ID, "caption": caption}, files={"document": (p.name, f)}, timeout=60)
            res.raise_for_status()
            self._log("telegram", settings.TELEGRAM_CHAT_ID, None, caption, attachment_path, True, None)
            return {"status": "sent"}
        except Exception as e:
            self._log("telegram", settings.TELEGRAM_CHAT_ID, None, caption, attachment_path, False, str(e))
            return {"status": "error", "error": str(e)}

    def _log(self, channel, target, subject, message, attachment, success, error):
        self.db.add(AlertLog(channel=channel, target=target, subject=subject, message=message, attachment_path=attachment, success=success, error=error))
        self.db.commit()

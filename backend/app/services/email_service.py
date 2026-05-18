import smtplib
from email.message import EmailMessage
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.fx_models import AlertLog

class EmailService:
    def __init__(self, db: Session):
        self.db = db

    def send_report(self, subject: str, body: str, attachment_path: str):
        targets = [x.strip() for x in settings.EMAIL_TO_LIST.split(",") if x.strip()]
        if not settings.SMTP_ENABLED:
            self._log("email", ",".join(targets), subject, body, attachment_path, False, "SMTP disabled")
            return {"status": "disabled"}

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_USER
        msg["To"] = ", ".join(targets)
        msg.set_content(body)

        p = Path(attachment_path)
        if p.exists():
            msg.add_attachment(p.read_bytes(), maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=p.name)

        try:
            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
                smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                smtp.send_message(msg)
            self._log("email", ",".join(targets), subject, body, attachment_path, True, None)
            return {"status": "sent", "targets": targets}
        except Exception as e:
            self._log("email", ",".join(targets), subject, body, attachment_path, False, str(e))
            return {"status": "error", "error": str(e)}

    def _log(self, channel, target, subject, message, attachment, success, error):
        self.db.add(AlertLog(channel=channel, target=target, subject=subject, message=message, attachment_path=attachment, success=success, error=error))
        self.db.commit()

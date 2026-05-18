from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FX AI Hub AI Advanced"
    DATABASE_URL: str = "sqlite:///./fx_ai_hub_advanced.db"
    AWESOME_API_BASE: str = "https://economia.awesomeapi.com.br"
    DEFAULT_PAIRS: str = "USD-BRL,EUR-BRL,KRW-BRL,JPY-BRL,CNY-BRL,GBP-BRL,ARS-BRL,BTC-BRL"
    KPW_ENABLED: bool = True
    KPW_MANUAL_BRL_VALUE: float = 0.0056
    KPW_SOURCE_NOTE: str = "manual_or_alternative_source_required"
    REPORTS_DIR: str = "reports"
    SMTP_ENABLED: bool = False
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_TO_LIST: str = ""
    TELEGRAM_ENABLED: bool = False
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    LLM_MODE: str = "mock"
    VLLM_BASE_URL: str = "http://localhost:8001/v1"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

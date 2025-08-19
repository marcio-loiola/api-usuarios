from pydantic import BaseModel
import os

class Settings(BaseModel):
	linkedin_email: str | None = os.getenv("LINKEDIN_EMAIL")
	linkedin_password: str | None = os.getenv("LINKEDIN_PASSWORD")
	telegram_bot_token: str | None = os.getenv("TELEGRAM_BOT_TOKEN")
	telegram_chat_id: str | None = os.getenv("TELEGRAM_CHAT_ID")
	smtp_host: str | None = os.getenv("SMTP_HOST")
	smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
	smtp_username: str | None = os.getenv("SMTP_USERNAME")
	smtp_password: str | None = os.getenv("SMTP_PASSWORD")
	email_to: str | None = os.getenv("EMAIL_TO")
	run_interval_minutes: int = int(os.getenv("RUN_INTERVAL_MINUTES", "15"))
	headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
	country_pref: list[str] = os.getenv("COUNTRY_PREF", "br,us").split(",")
	lang_pref: list[str] = os.getenv("LANG_PREF", "pt,en").split(",")

settings = Settings()

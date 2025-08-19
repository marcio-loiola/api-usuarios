from __future__ import annotations
import smtplib
from email.message import EmailMessage
import requests
from .config import settings
from .db import has_notified, mark_notified


def _send_email(subject: str, body: str) -> bool:
	if not (settings.smtp_host and settings.smtp_username and settings.smtp_password and settings.email_to):
		return False
	msg = EmailMessage()
	msg["Subject"] = subject
	msg["From"] = settings.smtp_username
	msg["To"] = settings.email_to
	msg.set_content(body)
	with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as s:
		s.starttls()
		s.login(settings.smtp_username, settings.smtp_password)
		s.send_message(msg)
	return True


def _send_telegram(text: str) -> bool:
	if not (settings.telegram_bot_token and settings.telegram_chat_id):
		return False
	url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
	payload = {"chat_id": settings.telegram_chat_id, "text": text, "disable_web_page_preview": True}
	r = requests.post(url, json=payload, timeout=20)
	return r.ok


def notify(job_id: str, title: str, url: str, summary: str) -> None:
	if not has_notified(job_id, "telegram"):
		if _send_telegram(f"Job alert: {title}\n{url}\n\n{summary}"):
			mark_notified(job_id, "telegram")
	if not has_notified(job_id, "email"):
		if _send_email(f"Job alert: {title}", f"{url}\n\n{summary}"):
			mark_notified(job_id, "email")

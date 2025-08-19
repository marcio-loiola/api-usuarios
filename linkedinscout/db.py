import sqlite3
from contextlib import contextmanager
from typing import Iterable, Tuple
from pathlib import Path

_DB_PATH = Path('/workspace/linkedinscout.db')

@contextmanager
def connect():
	conn = sqlite3.connect(_DB_PATH)
	conn.execute('PRAGMA journal_mode=WAL;')
	try:
		yield conn
	finally:
		conn.commit()
		conn.close()

SCHEMA = '''
CREATE TABLE IF NOT EXISTS job_posts (
	id TEXT PRIMARY KEY,
	url TEXT,
	title TEXT,
	company TEXT,
	location TEXT,
	work_model TEXT,
	experience_level TEXT,
	language TEXT,
	country TEXT,
	posted_at TEXT,
	content_text TEXT,
	requirements TEXT,
	technologies TEXT,
	created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS notifications (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	job_id TEXT,
	channel TEXT,
	sent_at TEXT DEFAULT CURRENT_TIMESTAMP
);
'''

def init_db():
	with connect() as c:
		c.executescript(SCHEMA)

def has_notified(job_id: str, channel: str) -> bool:
	with connect() as c:
		row = c.execute('SELECT 1 FROM notifications WHERE job_id=? AND channel=?', (job_id, channel)).fetchone()
		return row is not None

def mark_notified(job_id: str, channel: str):
	with connect() as c:
		c.execute('INSERT INTO notifications(job_id,channel) VALUES(?,?)', (job_id, channel))

def upsert_job(job: dict):
	with connect() as c:
		c.execute('''
		INSERT INTO job_posts(id,url,title,company,location,work_model,experience_level,language,country,posted_at,content_text,requirements,technologies)
		VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
		ON CONFLICT(id) DO UPDATE SET url=excluded.url,title=excluded.title,company=excluded.company,location=excluded.location,work_model=excluded.work_model,experience_level=excluded.experience_level,language=excluded.language,country=excluded.country,posted_at=excluded.posted_at,content_text=excluded.content_text,requirements=excluded.requirements,technologies=excluded.technologies;
		''', (job.get('id'),job.get('url'),job.get('title'),job.get('company'),job.get('location'),job.get('work_model'),job.get('experience_level'),job.get('language'),job.get('country'),job.get('posted_at'),job.get('content_text'),'
'.join(job.get('requirements',[])),'
'.join(job.get('technologies',[]))))


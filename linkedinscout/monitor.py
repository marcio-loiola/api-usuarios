import asyncio
from datetime import datetime
from typing import List, Tuple

from rich import print
from .matcher import score_exact_match, score_similar_job, EXACT_THRESHOLD, SIMILAR_THRESHOLD
from .db import init_db, upsert_job
from .notifier import notify

async def fake_linkedin_scan() -> List[Tuple[str, str]]:
	# MVP: No LinkedIn login in this step. Replace with real scraper later.
	return []

async def process_posts(posts: List[Tuple[str, str]]):
	for pid, text in posts:
		exact = score_exact_match(text)
		if exact >= EXACT_THRESHOLD:
			job = {
				'id': pid,
				'url': pid,
				'title': 'Frontend Jr',
				'company': None,
				'location': None,
				'work_model': 'Remote',
				'experience_level': 'Junior',
				'language': 'pt',
				'country': 'br',
				'posted_at': datetime.utcnow().isoformat(),
				'content_text': text,
				'requirements': [],
				'technologies': [],
			}
			upsert_job(job)
			notify(pid, 'Frontend Jr (Exact match)', pid, 'Exact target job identified')
			continue
		sim = score_similar_job(text)
		if sim['overall'] >= SIMILAR_THRESHOLD and sim['remote']:
			job = {
				'id': pid,
				'url': pid,
				'title': 'Similar frontend role',
				'company': None,
				'location': None,
				'work_model': 'Remote',
				'experience_level': 'Junior',
				'language': None,
				'country': None,
				'posted_at': datetime.utcnow().isoformat(),
				'content_text': text,
				'requirements': [],
				'technologies': [],
			}
			upsert_job(job)
			notify(pid, 'Similar job detected', pid, f"scores={sim}")

async def run_monitor():
	init_db()
	print('[bold green]LinkedIn monitor starting[/bold green]')
	posts = await fake_linkedin_scan()
	await process_posts(posts)

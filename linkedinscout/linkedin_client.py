from __future__ import annotations
import asyncio
import json
import re
from typing import List, Tuple, Dict
from pathlib import Path

from playwright.async_api import async_playwright, BrowserContext, Page
from .config import settings

_STORAGE = Path('/workspace/linkedinscout_storage.json')

CANDIDATE_LINK_RE = re.compile(r"https?://(?:www\.)?linkedin\.com/in/[^\s]+|https?://[^\s]+", re.I)

class LinkedInClient:
	def __init__(self) -> None:
		self.context: BrowserContext | None = None
		self.page: Page | None = None

	async def __aenter__(self) -> 'LinkedInClient':
		self.play = await async_playwright().start()
		browser = await self.play.chromium.launch(headless=settings.headless)
		if _STORAGE.exists():
			self.context = await browser.new_context(storage_state=str(_STORAGE))
		else:
			self.context = await browser.new_context()
		self.page = await self.context.new_page()
		return self

	async def __aexit__(self, exc_type, exc, tb):
		if self.context:
			await self.context.storage_state(path=str(_STORAGE))
			await self.context.close()
		if hasattr(self, 'play') and self.play:
			await self.play.stop()

	async def login_if_needed(self) -> None:
		assert self.page
		await self.page.goto('https://www.linkedin.com/feed/', wait_until='domcontentloaded')
		if 'login' in self.page.url and settings.linkedin_email and settings.linkedin_password:
			await self.page.fill('input[id=username]', settings.linkedin_email)
			await self.page.fill('input[id=password]', settings.linkedin_password)
			await self.page.click('button[type=submit]')
			await self.page.wait_for_load_state('networkidle')
			await asyncio.sleep(2)

	async def search_posts(self, query: str, max_posts: int = 30) -> List[Tuple[str, str, str]]:
		"""Return list of (id,url,text)."""
		assert self.page
		url = f'https://www.linkedin.com/search/results/content/?keywords={query}&origin=GLOBAL_SEARCH_HEADER'
		await self.page.goto(url, wait_until='domcontentloaded')
		collected: Dict[str, Tuple[str, str, str]] = {}
		for _ in range(20):
			cards = await self.page.locator('[data-urn], article').all()
			for c in cards:
				try:
					urn = await c.get_attribute('data-urn')
					text = await c.inner_text()
					plink = await c.locator('a').first.get_attribute('href')
					if not ur n:
						continue
					url_full = plink if plink and plink.startswith('http') else f'https://www.linkedin.com/feed/update/{urn}'
					collected[urn] = (urn, url_full, text)
				except Exception:
					pass
			await self.page.mouse.wheel(0, 2000)
			await asyncio.sleep(0.8)
			if len(collected) >= max_posts:
				break
		return list(collected.values())[:max_posts]

	async def extract_candidates_from_post(self, post_url: str) -> List[Tuple[str, str]]:
		assert self.page
		await self.page.goto(post_url, wait_until='domcontentloaded')
		await asyncio.sleep(1.5)
		comments = await self.page.locator('[data-test-id="comment"] , .comments-comment-item').all()
		results: List[Tuple[str, str]] = []
		for item in comments:
			try:
				name = await item.locator('a[href*="/in/"]').first.inner_text()
				text = await item.inner_text()
				m = CANDIDATE_LINK_RE.search(text)
				if m:
					results.append((name, m.group(0)))
			except Exception:
				pass
		return results

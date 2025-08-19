from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Candidate(BaseModel):
	name: str
	profile_url: Optional[str] = None
	portfolio_url: Optional[str] = None

class JobPost(BaseModel):
	id: str = Field(..., description="Stable unique id (e.g., LinkedIn URN or URL)")
	url: str
	title: str
	company: Optional[str] = None
	location: Optional[str] = None
	work_model: Optional[str] = None
	experience_level: Optional[str] = None
	language: Optional[str] = None
	country: Optional[str] = None
	posted_at: Optional[datetime] = None
	content_text: str
	requirements: List[str] = []
	technologies: List[str] = []
	candidates: List[Candidate] = []

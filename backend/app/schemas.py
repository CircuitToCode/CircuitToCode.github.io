from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Any

class LoginInput(BaseModel):
    username: str
    password: str

class TokenOutput(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ProjectInput(BaseModel):
    slug: str = Field(min_length=2, max_length=120, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title: str = Field(min_length=2, max_length=180)
    description: str
    category: str
    technologies: list[str] = []
    status: str = "In progress"
    image_url: str | None = None
    gallery: list[str] = []
    github_url: str | None = None
    demo_url: str | None = None
    featured: bool = False
    sort_order: int = 0
    is_published: bool = True

class SkillInput(BaseModel):
    name: str
    category: str
    proficiency: int = Field(default=60, ge=0, le=100)
    sort_order: int = 0

class ExperienceInput(BaseModel):
    role: str
    company: str
    period: str
    location: str | None = None
    responsibilities: list[str] = []
    contributions: list[str] = []
    sort_order: int = 0

class AchievementInput(BaseModel):
    label: str
    detail: str
    metric: str | None = None
    sort_order: int = 0

class ProfileInput(BaseModel):
    value: dict[str, Any]

class ORMOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

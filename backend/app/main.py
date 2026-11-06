from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import select
from .config import get_settings
from .database import Base, engine, get_db
from . import models, schemas
from .security import verify_password, create_access_token, require_admin

settings = get_settings()
Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="1.0.0", description="Portfolio content and administration API")
app.add_middleware(CORSMiddleware, allow_origins=settings.allowed_origins, allow_credentials=True, allow_methods=["GET","POST","PUT","PATCH","DELETE"], allow_headers=["Authorization","Content-Type"])
upload_root = Path(settings.upload_dir)
upload_root.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=upload_root), name="uploads")

@app.get("/health")
def health():
    return {"status":"ok","service":settings.app_name}

@app.post("/api/v1/auth/login", response_model=schemas.TokenOutput)
def login(data: schemas.LoginInput):
    if data.username != settings.admin_username or not verify_password(data.password, settings.admin_password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"access_token":create_access_token(data.username)}

@app.get("/api/v1/projects")
def list_projects(category: str | None = None, search: str | None = None, db: Session = Depends(get_db)):
    query = select(models.Project).where(models.Project.is_published == True).order_by(models.Project.sort_order, models.Project.id.desc())
    if category: query = query.where(models.Project.category == category)
    rows = db.scalars(query).all()
    if search:
        needle = search.casefold()
        rows = [p for p in rows if needle in p.title.casefold() or needle in p.description.casefold() or any(needle in t.casefold() for t in p.technologies)]
    return rows

@app.get("/api/v1/projects/{slug}")
def get_project(slug: str, db: Session = Depends(get_db)):
    row = db.scalar(select(models.Project).where(models.Project.slug == slug, models.Project.is_published == True))
    if not row: raise HTTPException(404, "Project not found")
    return row

@app.get("/api/v1/skills")
def list_skills(db: Session = Depends(get_db)):
    return db.scalars(select(models.Skill).order_by(models.Skill.category, models.Skill.sort_order)).all()

@app.get("/api/v1/experience")
def list_experience(db: Session = Depends(get_db)):
    return db.scalars(select(models.Experience).order_by(models.Experience.sort_order)).all()

@app.get("/api/v1/achievements")
def list_achievements(db: Session = Depends(get_db)):
    return db.scalars(select(models.Achievement).order_by(models.Achievement.sort_order)).all()

@app.get("/api/v1/profile/{key}")
def get_profile(key: str, db: Session = Depends(get_db)):
    row = db.scalar(select(models.SiteProfile).where(models.SiteProfile.key == key))
    if not row: raise HTTPException(404, "Profile section not found")
    return row.value

@app.post("/api/v1/admin/projects", status_code=201)
def create_project(data: schemas.ProjectInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    if db.scalar(select(models.Project).where(models.Project.slug == data.slug)): raise HTTPException(409, "Project slug already exists")
    row = models.Project(**data.model_dump()); db.add(row); db.commit(); db.refresh(row); return row

@app.put("/api/v1/admin/projects/{project_id}")
def update_project(project_id: int, data: schemas.ProjectInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.get(models.Project, project_id)
    if not row: raise HTTPException(404, "Project not found")
    for key, value in data.model_dump().items(): setattr(row, key, value)
    db.commit(); db.refresh(row); return row

@app.delete("/api/v1/admin/projects/{project_id}", status_code=204)
def delete_project(project_id: int, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.get(models.Project, project_id)
    if not row: raise HTTPException(404, "Project not found")
    db.delete(row); db.commit(); return None

@app.post("/api/v1/admin/skills", status_code=201)
def create_skill(data: schemas.SkillInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=models.Skill(**data.model_dump()); db.add(row); db.commit(); db.refresh(row); return row

@app.put("/api/v1/admin/skills/{item_id}")
def update_skill(item_id: int, data: schemas.SkillInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(models.Skill,item_id)
    if not row: raise HTTPException(404,"Skill not found")
    for k,v in data.model_dump().items(): setattr(row,k,v)
    db.commit(); db.refresh(row); return row

@app.delete("/api/v1/admin/skills/{item_id}", status_code=204)
def delete_skill(item_id: int, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(models.Skill,item_id)
    if not row: raise HTTPException(404,"Skill not found")
    db.delete(row); db.commit(); return None

@app.post("/api/v1/admin/experience", status_code=201)
def create_experience(data: schemas.ExperienceInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=models.Experience(**data.model_dump()); db.add(row); db.commit(); db.refresh(row); return row

@app.put("/api/v1/admin/experience/{item_id}")
def update_experience(item_id: int, data: schemas.ExperienceInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(models.Experience,item_id)
    if not row: raise HTTPException(404,"Experience not found")
    for k,v in data.model_dump().items(): setattr(row,k,v)
    db.commit(); db.refresh(row); return row

@app.delete("/api/v1/admin/experience/{item_id}", status_code=204)
def delete_experience(item_id: int, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(models.Experience,item_id)
    if not row: raise HTTPException(404,"Experience not found")
    db.delete(row); db.commit(); return None

@app.post("/api/v1/admin/achievements", status_code=201)
def create_achievement(data: schemas.AchievementInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=models.Achievement(**data.model_dump()); db.add(row); db.commit(); db.refresh(row); return row

@app.put("/api/v1/admin/achievements/{item_id}")
def update_achievement(item_id: int, data: schemas.AchievementInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(models.Achievement,item_id)
    if not row: raise HTTPException(404,"Achievement not found")
    for k,v in data.model_dump().items(): setattr(row,k,v)
    db.commit(); db.refresh(row); return row

@app.delete("/api/v1/admin/achievements/{item_id}", status_code=204)
def delete_achievement(item_id: int, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.get(models.Achievement,item_id)
    if not row: raise HTTPException(404,"Achievement not found")
    db.delete(row); db.commit(); return None

@app.put("/api/v1/admin/profile/{key}")
def update_profile(key: str, data: schemas.ProfileInput, _: str = Depends(require_admin), db: Session = Depends(get_db)):
    row=db.scalar(select(models.SiteProfile).where(models.SiteProfile.key == key))
    if not row: row=models.SiteProfile(key=key, value=data.value); db.add(row)
    else: row.value=data.value
    db.commit(); db.refresh(row); return row.value

@app.post("/api/v1/admin/uploads", status_code=201)
async def upload_asset(file: UploadFile = File(...), _: str = Depends(require_admin)):
    allowed={"image/jpeg","image/png","image/webp","application/pdf"}
    if file.content_type not in allowed: raise HTTPException(415,"Only JPG, PNG, WebP and PDF files are allowed")
    content=await file.read(settings.max_upload_mb*1024*1024+1)
    if len(content)>settings.max_upload_mb*1024*1024: raise HTTPException(413,"File exceeds upload limit")
    suffix=Path(file.filename or "").suffix.lower()
    if suffix not in {".jpg",".jpeg",".png",".webp",".pdf"}: raise HTTPException(415,"Unsupported file extension")
    name=f"{uuid4().hex}{suffix}"; (upload_root/name).write_bytes(content)
    return {"filename":name,"url":f"/uploads/{name}","size":len(content)}


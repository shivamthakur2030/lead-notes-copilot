from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
from database import engine, SessionLocal
from schemas import LeadCreate, LeadResponse, LeadUpdate, NoteCreate, NoteResponse

app = FastAPI(title="Lead Notes Copilot")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Lead Notes Copilot API"}


@app.post("/leads", response_model=LeadResponse)
def create_lead(
    lead: LeadCreate,
    db: Session = Depends(get_db)
):
    db_lead = models.LeadDB(**lead.model_dump())

    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)

    return db_lead


@app.get("/leads", response_model=list[LeadResponse])
def get_leads(
    search: str | None = None,
    company: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(models.LeadDB)

    if search:
        query = query.filter(
            models.LeadDB.name.ilike(f"%{search}%")
        )

    if company:
        query = query.filter(
            models.LeadDB.company.ilike(f"%{company}%")
        )

    return query.offset(offset).limit(limit).all()


@app.get("/leads/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.LeadDB).filter(
        models.LeadDB.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return lead


@app.patch("/leads/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    updates: LeadUpdate,
    db: Session = Depends(get_db)
):
    lead = db.query(models.LeadDB).filter(
        models.LeadDB.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    update_data = updates.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(lead, field, value)

    db.commit()
    db.refresh(lead)

    return lead


@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.LeadDB).filter(
        models.LeadDB.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    db.delete(lead)
    db.commit()

    return {"message": "Lead deleted successfully"}

@app.post("/leads/{lead_id}/notes", response_model=NoteResponse)
def create_note(
    lead_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    lead = db.query(models.LeadDB).filter(
        models.LeadDB.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    db_note = models.NoteDB(
        lead_id=lead_id,
        content=note.content
    )

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note

@app.get("/leads/{lead_id}/notes", response_model=list[NoteResponse])
def get_notes(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.LeadDB).filter(
        models.LeadDB.id == lead_id
    ).first()

    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    return (
        db.query(models.NoteDB)
        .filter(models.NoteDB.lead_id == lead_id)
        .order_by(models.NoteDB.id.desc())
        .all()
    )

@app.get("/analytics/overview")
def analytics_overview(db: Session = Depends(get_db)):
    total_leads = db.query(models.LeadDB).count()
    total_notes = db.query(models.NoteDB).count()

    leads_without_notes = (
        db.query(models.LeadDB)
        .filter(~models.LeadDB.notes.any())
        .count()
    )

    return {
        "total_leads": total_leads,
        "total_notes": total_notes,
        "leads_without_notes": leads_without_notes
    }

@app.get("/analytics/notes-per-lead")
def notes_per_lead(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.LeadDB.id.label("lead_id"),
            models.LeadDB.name,
            func.count(models.NoteDB.id).label("total_notes")
        )
        .outerjoin(
            models.NoteDB,
            models.LeadDB.id == models.NoteDB.lead_id
        )
        .group_by(models.LeadDB.id, models.LeadDB.name)
        .all()
    )

    return [
        {
            "lead_id": row.lead_id,
            "name": row.name,
            "total_notes": row.total_notes
        }
        for row in results
    ]


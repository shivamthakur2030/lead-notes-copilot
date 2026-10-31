from pydantic import BaseModel, ConfigDict, EmailStr, Field
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    company: str

class LeadResponse(LeadCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)

class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

class NoteCreate(BaseModel):
    content: str = Field(min_length=1)

class NoteResponse(NoteCreate):
    id: int
    lead_id: int

    model_config = ConfigDict(from_attributes=True)

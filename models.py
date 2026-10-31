from sqlalchemy import Column, ForeignKey, String, Integer, Text
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()

class LeadDB(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    company = Column(String, nullable=False)

    notes: Mapped[list["NoteDB"]] = relationship(
    back_populates="lead",
    cascade="all, delete-orphan"
    )

class NoteDB(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lead_id: Mapped[int] = mapped_column(
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    lead: Mapped["LeadDB"] = relationship(back_populates="notes")

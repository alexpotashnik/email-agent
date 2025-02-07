from datetime import datetime
from enum import StrEnum
from typing import TypeVar, List

from sqlalchemy import Column, ForeignKey, String, Integer, Enum, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Idable(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


_ORM_ENUM = {
    'values_callable': lambda t: [e.value for e in t],
    'native_enum': False
}


IdableType = TypeVar('IdableType', bound=Idable)


class Client(Idable):
    __tablename__ = "clients"

    name: Mapped[str] = mapped_column(String, nullable=False)
    def __repr__(self):
        return f'[{self.id}] {self.name}'


class DealStatus(StrEnum):
    ACTIVE = 'active'
    STALE = 'stale'
    CONCLUDED = 'concluded'


class Deal(Idable):
    __tablename__ = "deals"

    address: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[DealStatus] = mapped_column(Enum(DealStatus, **_ORM_ENUM), unique=False)

    events: Mapped[List['Event']] = relationship('Event', back_populates='deal')


class Engagement(Idable):
    __tablename__ = "engagements"

    buyer_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    counterparty: Mapped[str] = mapped_column(String, nullable=False)

    buyer: Mapped["Client"] = relationship("Client", foreign_keys=[buyer_id])
    seller: Mapped["Client"] = relationship("Client", foreign_keys=[seller_id])


class Conversation(Idable):
    __tablename__ = "conversations"

    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id"), nullable=True)
    attributes: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    client: Mapped["Client"] = relationship("Client")
    deal: Mapped["Deal"] = relationship("Deal")


class Event(Idable):
    __tablename__ = "events"

    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id"), nullable=True)
    attributes: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    deal = relationship("Deal", back_populates="events")


class PromptTemplate(Idable):
    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

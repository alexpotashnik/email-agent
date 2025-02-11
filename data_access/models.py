from datetime import datetime
from enum import StrEnum
from typing import TypeVar, List, Optional

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
    __tablename__ = 'client'

    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    def __repr__(self):
        return f'[{self.id}] {self.name}: {self.email}'


class EngagementStatus(StrEnum):
    PROSPECT = 'prospect'
    ACTIVE = 'active'
    STALE = 'stale'
    CONCLUDED = 'concluded'


class Engagement(Idable):
    __tablename__ = 'engagement'

    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'), nullable=False)
    counterparty_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    counterparty_email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    property_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[EngagementStatus] = mapped_column(Enum(EngagementStatus, **_ORM_ENUM), unique=False)

    client: Mapped['Client'] = relationship('Client', foreign_keys=[client_id])
    events: Mapped[List['Event']] = relationship('Event', back_populates='engagement')

    def __repr__(self):
        optionals = [o for o in [self.counterparty_email, self.counterparty_name, self.property_address] if o]
        optionals_repr = f'({', '.join(optionals)})' if optionals else ''
        return f'[{self.id}] {self.client.name}: {self.status.name}' + optionals_repr



class Conversation(Idable):
    __tablename__ = 'conversation'

    client_id: Mapped[int] = mapped_column(ForeignKey('client.id'), nullable=False)
    engagement_id: Mapped[int] = mapped_column(ForeignKey('engagement.id'), nullable=False)
    attributes: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    client: Mapped['Client'] = relationship('Client')
    deal: Mapped['Engagement'] = relationship('Engagement')


class EventType(StrEnum):
    OUTBOUND_EMAIL = 'outbound_email'
    CUSTOMER_EMAIL = 'customer_email'
    COUNTERPARTY_EMAIL = 'customer_email'
    OUTREACH_TIMEOUT = 'outreach_timeout'


class Event(Idable):
    __tablename__ = 'event'

    engagement_id: Mapped[int] = mapped_column(ForeignKey('engagement.id'), nullable=True)
    attributes: Mapped[dict] = mapped_column(JSON, nullable=False)
    type: Mapped[EventType] = mapped_column(Enum(EventType, **_ORM_ENUM), unique=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    engagement = relationship('Engagement', back_populates='events')

    def __repr__(self):
        return f'[{self.id}, {self.type.name}, {self.timestamp}] {self.engagement.client.name}: {self.attributes}'

class PromptTemplate(Idable):
    __tablename__ = 'prompt_templates'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Type, List, Dict

from sqlalchemy import create_engine, select, desc, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from data_access.models import Idable, IdableType, Client, Engagement, EngagementStatus, EventType, Event



class DataStore:
    @classmethod
    @contextmanager
    def get(cls, connection_str: Optional[str]) -> DataStore:
        engine = create_engine(connection_str)
        Idable.metadata.create_all(engine)
        session = scoped_session(sessionmaker(autoflush=True, bind=engine))()
        try:
            yield cls(session)
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    def __init__(self, db: Session):
        self._db = db

    def _list(self, type: Type[IdableType]) -> List[IdableType]:
        return  [row[0] for row in self._db.execute(select(type))]

    def cache_clear(self):
        self._list.cache_clear()  # type: ignore

    def clear(self):
        engine = self._db.connection().engine
        Idable.metadata.drop_all(engine)
        Idable.metadata.create_all(engine)

    def create_client(self, name, email) -> Client:
        client = Client(name=name, email=email)
        self._db.add(client)
        self._db.flush()
        return client

    def list_clients(self):
        return self._list(Client)

    def create_engagement(self, client: Client):
        engagement = Engagement(client_id=client.id, status=EngagementStatus.ACTIVE)
        # counterparty_name: Mapped[str] = mapped_column(String)
        # counterparty_email: Mapped[str] = mapped_column(String)
        # property_address: Mapped[str] = mapped_column(String)
        self._db.add(engagement)
        self._db.flush()
        return engagement

    def list_engagements(self):
        return self._list(Engagement)

    def create_event(self, engagement: Engagement, type: EventType, attributes: Dict):
        event = Event(engagement_id=engagement.id,
                      type=type,
                      timestamp=datetime.now(),
                      attributes=attributes)
        self._db.add(event)
        self._db.flush()
        return event

    def list_events(self):
        return self._list(Event)


from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Type, List, Dict

from sqlalchemy import create_engine, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from data_access.models import Idable, IdableType, Client, Engagement, Event, EventType



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

    def _find(self, type: Type[IdableType], id: int) -> Optional[IdableType]:
        if not (idable := self._db.query(type).filter(type.id == id).one()):
            raise Exception(f'{type.__name__} {id} not found')
        return idable

    def _list(self, type: Type[IdableType], condition = None) -> List[IdableType]:
        query = self._db.query(type)
        if condition is not None:
            query = query.filter(condition)
        return query.all()

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
        engagement = Engagement(client_id=client.id)
        self._db.add(engagement)
        self._db.flush()
        return engagement

    def find_engagement(self, id: int):
        return self._find(Engagement, id)

    def list_engagements(self):
        return self._list(Engagement)

    def update_engagement(self,
                          engagement_id: int,
                          counterparty_name: str,
                          counterparty_email: str,
                          property_address: str):
        if not (engagement := self._db.query(Engagement).filter(Engagement.id == engagement_id).first()):
            raise Exception(f'Engagement {engagement_id} not found')

        engagement.counterparty_name = counterparty_name
        engagement.counterparty_email = counterparty_email
        engagement.property_address = property_address
        self._db.commit()
        self._db.flush()
        return engagement


    def create_event(self, engagement: Engagement, type: EventType, attributes: Dict = None):
        event = Event(engagement_id=engagement.id,
                      type=type,
                      timestamp=datetime.now(),
                      attributes=attributes or {})
        self._db.add(event)
        self._db.flush()
        return event

    def list_events(self, engagement: Engagement):
        return self._list(Event, Event.engagement == engagement)

    def find_last_event(self, engagement: Engagement) -> Optional[Event]:
        return self._db.query(Event)\
            .filter(Event.engagement_id == engagement.id)\
            .order_by(desc(Event.timestamp))\
            .first()

    def get_event(self, event_id: int) -> Event:
        return self._db.query(Event).filter(Event.id == event_id).one()  # type: ignore


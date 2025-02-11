from contextlib import contextmanager
from datetime import datetime
from typing import Optional, Type, List

from sqlalchemy import create_engine, select, desc, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from data_access.models import Idable, IdableType, Client, Engagement, EngagementStatus, EventType, Event


class DataStore:
    @contextmanager
    def _get_session(self, leave_open: Optional[bool] = False) -> Session:
        session = Session(self._engine)
        try:
            yield session
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            if not leave_open:
                session.commit()
                session.close()

    def __init__(self, connection_str: Optional[str] = None):
        self._engine = create_engine(connection_str)
        Idable.metadata.create_all(self._engine)

    def _list(self, type: Type[IdableType]) -> List[IdableType]:
        with self._get_session(leave_open=True) as session:
            return  [row[0] for row in session.execute(select(type))]

    def cache_clear(self):
        self._list.cache_clear()  # type: ignore

    def clear(self):
        with self._get_session():
            Idable.metadata.drop_all(self._engine)
            Idable.metadata.create_all(self._engine)

    def create_client(self, name, email) -> Client:
        client = Client(name=name, email=email)
        with self._get_session(leave_open = True) as session:
            session.add(client)
            session.commit()
            session.refresh(client)
        return client

    def list_clients(self):
        return self._list(Client)

    def create_engagement(self, client: Client):
        engagement = Engagement(client_id=client.id, status=EngagementStatus.ACTIVE)
        # counterparty_name: Mapped[str] = mapped_column(String)
        # counterparty_email: Mapped[str] = mapped_column(String)
        # property_address: Mapped[str] = mapped_column(String)
        with self._get_session(leave_open = True) as session:
            session.add(engagement)
            session.commit()
            session.refresh(engagement)
        return engagement

    def list_engagements(self):
        return self._list(Engagement)

    def create_event(self, engagement: Engagement, type: EventType):
        event = Event(engagement_id=engagement.id,
                      type=type,
                      timestamp=datetime.now(),
                      attributes={'attrib1': 1, 'attrib2': ['val1', 'value2']})
        with self._get_session(leave_open = True) as session:
            session.add(event)
            session.commit()
            session.refresh(event)
        return event

    def list_events(self):
        return self._list(Event)


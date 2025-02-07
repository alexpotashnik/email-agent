from contextlib import contextmanager
from typing import Optional, Type, List

from sqlalchemy import create_engine, select, desc, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from data_access.models import Idable, IdableType


class DataStore:
    @contextmanager
    def _get_session(self, leave_open: Optional[bool] = False) -> Session:
        session = Session(self._engine)
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise
        finally:
            if not leave_open:
                session.close()

    def __init__(self, connection_str: Optional[str] = None):
        self._engine = create_engine(connection_str)
        Idable.metadata.create_all(self._engine)

    def _list(self, type: Type[IdableType]) -> List[IdableType]:
        with self._get_session() as session:
            return [row[0] for row in session.execute(select(type))]

    def cache_clear(self):
        self._list.cache_clear()  # type: ignore

    def clear(self):
        with self._get_session():
            Idable.metadata.drop_all(self._engine)
            Idable.metadata.create_all(self._engine)

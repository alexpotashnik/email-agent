from typing import TypeVar

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Idable(DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


IdableType = TypeVar('IdableType', bound=Idable)


class Customer(Idable):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


class Deal(Idable):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String, nullable=False)


class Engagement(Idable):
    __tablename__ = "engagements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    buyer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    other_party_name: Mapped[str] = mapped_column(String, nullable=False)

    buyer: Mapped["Customer"] = relationship("Customer", foreign_keys=[buyer_id])
    seller: Mapped["Customer"] = relationship("Customer", foreign_keys=[seller_id])


class Conversation(Idable):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    deal_id: Mapped[int] = mapped_column(ForeignKey("deals.id"), nullable=False)

    customer: Mapped["Customer"] = relationship("Customer")
    deal: Mapped["Deal"] = relationship("Deal")


class PromptTemplate(Idable):
    __tablename__ = "prompt_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

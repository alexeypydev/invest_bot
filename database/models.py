
from sqlalchemy import DateTime, Integer, String, func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class ShortProjects(Base):
    __tablename__ = 'ShortProjects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    cost: Mapped[int] = mapped_column(Integer)
    profit: Mapped[int] = mapped_column(Integer)
    guarantee: Mapped[str] = mapped_column(String(50))
    result_date: Mapped[DateTime] = mapped_column(DateTime)
    deadline_date: Mapped[DateTime] = mapped_column(DateTime)
    place: Mapped[int] = mapped_column(Integer, default=None)
    status: Mapped[str] = mapped_column(String(50))


class Users(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))


class LongProjects(Base):
    __tablename__ = 'LongProjects'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('Users.id'))
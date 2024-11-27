from sqlalchemy import BigInteger, String, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engin = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engin)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)


class Table(Base):
    __tablename__ = 'tables'

    id: Mapped[int] = mapped_column(primary_key=True)
    table_number: Mapped[int] = mapped_column()
    description: Mapped[str] = mapped_column(String(255))


class Availability(Base):
    __tablename__ = 'availability'

    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('tables.id'))
    date: Mapped[Date] = mapped_column(Date, nullable=True)
    hour: Mapped[int] = mapped_column()
    is_occupied: Mapped[bool] = mapped_column(default=False, server_default="0")
    occupied_now: Mapped[bool] = mapped_column(default=False, server_default="0")


async def async_mainbd():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

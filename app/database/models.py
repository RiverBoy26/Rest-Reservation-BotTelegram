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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    number_of_seats: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(255))


class Tables_is_occupied_now(Base):
    __tablename__ = 'tables_occupancy'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('tables.table_number'))
    occupied_now: Mapped[bool] = mapped_column(default=False, server_default="0")


class Table_reservation(Base):
    __tablename__ = 'tables_reservation'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    table_id: Mapped[int] = mapped_column(ForeignKey('tables.table_number'))
    surname: Mapped[str] = mapped_column(String(255))
    hour: Mapped[int] = mapped_column(nullable=False)
    end_hour: Mapped[int] = mapped_column(nullable=False)
    minutes: Mapped[int] = mapped_column(nullable=False)
    end_minutes: Mapped[int] = mapped_column(nullable=False)
    is_occupied: Mapped[bool] = mapped_column(default=True, server_default="1")


async def async_mainbd():
    async with engin.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

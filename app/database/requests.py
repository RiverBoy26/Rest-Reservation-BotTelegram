from app.database.models import async_session
from app.database.models import User, Table, Availability
from sqlalchemy import select


# Добавление пользователя в бд
async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        try:
            user = await session.scalar(select(User).where(User.tg_id == tg_id))

            if not user:
                session.add(User(tg_id=tg_id))
                await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


# Получение всей информации о столиках (id, описание)
async def get_tables():
    async with async_session() as session:
        tables = await session.scalars(select(Table))
        return tables.all()

# Получение bool столик занят по времени или нет
async def get_is_occupied(table_id):
    async with async_session() as session:
        result = await session.scalar(
            select(Availability).where(
                Availability.table_id == table_id,
                Availability.is_occupied is True
            )
        )
        return result is not None


# Получение bool столик занят на данный момент или нет
async def get_is_occupied_now(table_id):
    async with async_session() as session:
        result = await session.scalar(
            select(Availability).where(
                Availability.table_id == table_id,
                Availability.occupied_now is True
            )
        )
        return result is not None


async def get_tables_with_status():
    async with async_session() as session:
        query = (
            select(Table, Availability.is_occupied, Availability.occupied_now)
            .join(Availability, Table.id == Availability.table_id, isouter=True)
        )
        result = await session.execute(query)

        tables = []
        for table, is_occupied, occupied_now in result:
            status = "свободен"
            if is_occupied:
                status = "забронирован"
            if occupied_now:
                status = "занят"
            tables.append({
                "id": table.id,
                "description": table.description,
                "status": status
            })
        return tables

from app.database.models import async_session
from app.database.models import User, Table, Tables_is_occupied_now, Table_reservation
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
        tables = await session.scalars(select(Table).order_by(Table.table_number))
        return tables.all()

async def get_is_occupied_now(table_id):
    async with async_session() as session:
        result = await session.scalar(
            select(Tables_is_occupied_now).where(
                Tables_is_occupied_now.table_id == table_id,
                Tables_is_occupied_now.occupied_now is True
            )
        )
        return result is not None


async def set_table(table_id: int, number_of_seats: int, description: str):
    async with async_session() as session:
        table = Table(table_number=table_id, number_of_seats=number_of_seats, description=description)
        session.add(table)
        is_occupied_now = Tables_is_occupied_now(table_id=table_id)
        session.add(is_occupied_now)
        await session.commit()

async def delete_table(table_id: int):
    async with async_session() as session:
        table_to_delete = await session.get(Table, table_id)
        await session.delete(table_to_delete)
        is_occupied_now_delete = await session.get(Tables_is_occupied_now, table_id)
        await session.delete(is_occupied_now_delete)
        await session.commit()
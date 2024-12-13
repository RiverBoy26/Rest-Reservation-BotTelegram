from app.database.models import async_session
from app.database.models import User, Table, Tables_is_occupied_now, Table_reservation
from sqlalchemy import select
from sqlalchemy.sql import update


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
                Tables_is_occupied_now.occupied_now == 1
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


async def set_reservation(table_id: int, hour: int, minute: int):
    async with async_session() as session:
        set_table_reservation = Table_reservation(table_id=table_id, hour=hour, minutes=minute)
        session.add(set_table_reservation)
        await session.commit()


async def get_reservation(table_id: int):
    async with async_session() as session:
        table = await session.scalars(select(Table_reservation).where(Table_reservation.table_id == table_id).order_by(Table_reservation.hour))

        reservation_info = table.all()

        if len(reservation_info) == 0:
            return "Отсутствует расписание"
        tbl_info = "".join([f"Забронирован на {t.hour}:{t.minutes}\n" for t in reservation_info])
        return tbl_info


async def get_time_reservation(table_id: int):
    async with async_session() as session:
        table = await session.scalars(select(Table_reservation).where(Table_reservation.table_id == table_id).order_by(Table_reservation.hour))

        reservation_info = table.all()

        tbl_info = []
        for r in reservation_info:
            tbl_info.append(f"{r.hour}:{r.minutes}")
        return tbl_info


async def delete_reservation(table_id: int, d_time: str):
    async with async_session() as session:
        hour = int(d_time[0] + d_time[1])
        minutes = int(d_time[3] + d_time[4])

        query = (select(Table_reservation).where(
                    Table_reservation.table_id == table_id,
                    Table_reservation.hour == hour,
                    Table_reservation.minutes == minutes
                    ))
        result = await session.execute(query)
        reservation_to_delete = result.scalar_one_or_none()
        await session.delete(reservation_to_delete)
        await session.commit()

async def set_status_free(table_id: int):
    async with async_session() as session:
        status_update = (update(Tables_is_occupied_now).values(occupied_now=0).where(Tables_is_occupied_now.table_id == table_id))
        await session.execute(status_update)
        await session.commit()

async def set_status_busy(table_id: int):
    async with async_session() as session:
        status_update = (update(Tables_is_occupied_now).values(occupied_now=1).where(Tables_is_occupied_now.table_id == table_id))
        await session.execute(status_update)
        await session.commit()
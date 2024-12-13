import time
import datetime
import app.database.requests as rq

def isTimeFormat(input):
    try:
        time.strptime(input, '%H %M')
        return True
    except ValueError:
        return False
    
async def get_nearest_time(table_id):
    lst_time = await rq.get_time_reservation(table_id)
    now = datetime.datetime.now()
    for t in lst_time:
        booking_datetime = datetime.datetime.strptime(t, "%H:%M")
        booking_datetime = now.replace(hour=booking_datetime.time().hour,
                                       minute=booking_datetime.time().minute)
        if (now < booking_datetime):
            fin = await rq.get_time_surname_and_chrono(table_id, booking_datetime.hour, booking_datetime.minute)
            return f"{booking_datetime.strftime('%H:%M')}, {fin}"
    return "отсутствует"
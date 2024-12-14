# Rest-Reservation-BotTelegram
____

## Оглавление
- [Rest-Reservation-BotTelegram](#rest-reservation-bottelegram)
  - [Оглавление](#оглавление)
  - [Стек технологий](#стек-технологий)
  - [Краткое описание проекта](#краткое-описание-проекта)
  - [Установка и запуск](#установка-и-запуск)
  - [Команда разработки](#команда-разработки)

 ## Стек технологий
+ Python 3.12
+ Aiogram
+ Aiosqlite
+ SQL Alchemy
 ## Краткое описание проекта
Rest-Reservation-BotTelegram — Telegram-бот для сотрудников общепита. Бот позволяет вести учет столиков с нумерацией и предоставляет возможность их бронирования. Для каждого столика можно указывать статус: "занят" или "свободен", что облегчает отслеживание и управление бронью. При бронировании указываются фамилия клиента и продолжительность брони.
 ## Установка и запуск
1.Клонировать репозиторий и перейти к проекту:
   ```
   git clone https://github.com/RiverBoy26/Rest-Reservation-BotTelegram
   ```

2.В корневой директории проекта создайте виртуальное окружение, используя команду:
- Если у вас windows:
  
   ```
   python -m venv venv
   ```
    или

    ```
    py -3 -m venv venv
    ```
- Если у вас Linux/macOS:
  ```
  python3 -m venv venv
  ```

3.Активируйте виртуальное окружение командой:
- Если у вас windows:
  ```
  source venv/Scripts/activate
  ```
- Если у вас Linux/macOS:
  ```
  source venv/bin/activate
  ```
4.Обновите менеджер пакетов:
```
python -m pip install --upgrade pip
```
5.Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
6.Создайте файл .env и укажите токен вашего бота 
```
Token = *Ваш токен*
```
7.Запустить бота:
```
python main.py
```

## Команда разработки

- Deryabina Maria
  -  github: [sunnerfuer](https://github.com/sunnerfuer)

- Sokolov Mark
  -  github: [MarikSmerch](https://github.com/MarikSmerch)

- Ledovskikh Artem
  -  github: [RiverBoy26](https://github.com/RiverBoy26)

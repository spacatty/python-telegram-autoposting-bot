# Автопостинг бот

Задача бота: polling сообщений от каналов, заданных в .env (см. env.sample), фильтрация сообщений по ключевым словам и символам (реклама, ://, @ и т.д) с целью избежания пересылания рекламных постов.

Для того, чтобы бот слушал приватные группы, его туда нужно добавить.

Список использованных технологий/библиотек:
База данных: sqlite
TG-клиент: telethon
Отложенные задачи: AsyncIOScheduler

После установки переменных окружения, потребуется первоначальная авторизация в Telegram, которая запросит номер телефона и код доступа. После этого будет сгенерирован .session файл и бот будет готов к работе.

Polling-интервалы устанавливаются на 66-67 строках main.py:

```python
poll_scheduler.add_job(poll_messages, 'interval', seconds=10)
poll_scheduler.add_job(send_messages, 'interval', seconds=5)
```

## Развёртывание

1. Активация виртуального окружения venv:

```
./Scripts/activate
```

2. Установка зависимостей

```
pip install -r requirements.txt
```

3. Запуск

```
python main.py
```
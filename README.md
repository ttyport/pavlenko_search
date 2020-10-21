# Pavlenko Search Bot

Telegram бот для поиска видео с [YouTube канала Антона Павленко](https://www.youtube.com/channel/UC_hvS-IJ_SY04Op14v3l4Lg) по названию.

## Структура проекта

```
.
├── bot.py               - Файл с ботом
├── config.py            - Файл конфигурации
├── README.md            - Этот файл
└── requirements.txt     - Файл со списком зависимостей
```

## Запуск

Подразумевается, что у вас в системе установлен [Python3](https://python.org).

Сначала установим зависимости:

```
pip install -r requirements.txt
```

Теперь нужно [создать бота и получить его токен](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram/).
Далее нужно [получить ключ API YouTube](https://www.slickremix.com/docs/get-api-key-for-youtube/) и вписать оба значения в файл `config.py`

После этого можно запустить бота командой `python3 bot.py`.

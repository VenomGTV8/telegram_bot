# Telegram_Bot

## Формальное описание

Приветственное сообщение бота:

```
Привет! Я бот, который поможет не забыть прочитать статьи, найденные тобой в интернете :)
- Чтобы я запомнил статью, достаточно передать мне ссылку на нее. К примеру https://example.com
- Чтобы получить случайную статью, достаточно передать мне команду /get_article.
Но помни! Отдавая статью тебе на прочтение, она больше не хранится в моей базе. Так что тебе точно нужно её изучить
```

Данное сообщение увидит пользователь после начала взаимодействия с ботом (после команды /start). В данном сообщении указан функционал бота, которым можно пользоваться.

## Установка ПО для работы приложения

1. Установить интерпретатор python версии 3.11 или выше.
2. В папке с файлами приложения создать виртуальное окружение с помощью консольной команды `python -m venv {venv name}`, после чего активировать его командой `venv\Scripts\activate.bat` для Windows или `source venv/bin/activate` для Linux и MacOS.
3. Установить требуемые библиотеки в активированное виртуальное окружение командой `pip install -r requirements.txt`
4. Создать файл .env, открыть в любом текстовом редакторе и записать туда следующую строку:
```
API_TOKEN = ваш_api_token
```
где ваш_api_token - токен для телеграмм бота, который нужно получить от телеграмма. 
5. Для запуска приложения введите команду `python main.py` в консоли, открытой в папке с фалами приложения.

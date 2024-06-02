import sqlite3
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")


def connect_db():
    return sqlite3.connect("links.db")


def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            url TEXT,
            UNIQUE(user_id, url)
        )
    """
    )
    conn.commit()
    conn.close()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = update.message.text
    urls = [
        word
        for word in message.split()
        if word.startswith("http://") or word.startswith("https://")
    ]

    if not urls:
        await update.message.reply_text("Сообщение не содержит ссылок.")
        return

    conn = connect_db()
    cursor = conn.cursor()

    for url in urls:
        try:
            cursor.execute(
                "INSERT INTO links (user_id, url) VALUES (?, ?)", (user_id, url)
            )
            conn.commit()
            await update.message.reply_text(f"Ссылка сохранена: {url}")
        except sqlite3.IntegrityError:
            await update.message.reply_text(
                f"Ссылка уже существует в базе данных: {url}"
            )

    conn.close()


async def get_article(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, url FROM links WHERE user_id = ? ORDER BY RANDOM() LIMIT 1",
        (user_id,),
    )
    result = cursor.fetchone()

    if result:
        link_id, url = result
        await update.message.reply_text(f"Вот ваша случайная ссылка: {url}")
        cursor.execute("DELETE FROM links WHERE id = ?", (link_id,))
        conn.commit()
    else:
        await update.message.reply_text("Нет ссылок в базе данных.")

    conn.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот, который поможет не забыть прочитать статьи, "
        "найденные тобой в интернете :)\n- Чтобы я запомнил статью, "
        "достаточно передать мне ссылку на нее. К примеру https://example.com"
        "\n- Чтобы получить случайную статью, достаточно передать мне команду "
        "/get_article."
        "\nНо помни! Отдавая статью тебе на прочтение, она больше не хранится в моей базе. "
        "Так что тебе точно нужно её изучить"
    )


def main() -> None:
    init_db()

    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_article", get_article))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    application.run_polling()


if __name__ == "__main__":
    main()

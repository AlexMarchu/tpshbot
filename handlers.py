from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ChatAction, ChatType
from dotenv import load_dotenv
import datetime

import random
import asyncio
import os

from services.github_service import get_team_commits

load_dotenv()

router = Router()
flag = False


async def setup_chat_action(message: Message, action: ChatAction=ChatAction.TYPING, duration: float=0.8):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=action)
    await asyncio.sleep(duration)


async def send_stats(message: Message):
    global flag
    flag = True

    while True:
        await asyncio.sleep(1)
        if str(datetime.datetime.now().time())[:8] == '09:00:00':
            REPOSITORIES = [
                {"owner": "mkulli", "name": "housing-filter-control-system"},
                {"owner": "Polina-Shupikova", "name": "NPI"},
                {"owner": "KelBro", "name": "ProjectTPSH"},
                {"owner": "PaulKlifgt", "name": "QR-Museum"},
            ]

            team_commits = await get_team_commits(REPOSITORIES)
            if team_commits:
                response = "<b>Отчет о продуктивности за сегодня:</b>\n"
                for repo_name, count in sorted(team_commits.items(), key=lambda x: -x[1]):
                    response += f"• 📦 {repo_name}: {count} коммитов\n"
                response += (
                    "\n🟢 Старший Брат одобряет вашу продуктивность. 🟢\n"
                    "Продолжайте в том же духе, товарищи.\n"
                    "Достойный труд будет вознагражден. 🪖"
                )
            else:
                response = (
                    "🛑 За сегодня коммитов не было. 🛑\n"
                    "<b>Старший Брат недоволен вашей бездеятельностью.</b>\n"
                    "Помните: безделье — это преступление.\n"
                    "🕵️‍♂️ Министерство любви уже в курсе."
                )
            await asyncio.sleep(1)
            await message.answer(response, parse_mode="HTML")


@router.message(CommandStart())
async def cmd_start(message: Message):
    global flag
    await setup_chat_action(message)
    if not flag:
        asyncio.create_task(send_stats(message))
    response = (
        f"Добро пожаловать, товарищ {message.from_user.full_name}.\n"
        "<b>Старший Брат наблюдает за тобой.</b> 🪖\n"
        "Война — это мир. Свобода — это рабство. Незнание — сила.\n"
        "Сообщите о всех подозрительных действиях. 🚨"
    )
    await message.answer(response, parse_mode="HTML")


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    now_time = datetime.datetime.now()
    wait_time = datetime.datetime.combine(now_time.date(), datetime.time(9, 0))

    if now_time > wait_time:
        wait_time += datetime.timedelta(days=1)

    time_delta = wait_time - now_time

    response = (
        "⏳ <b>Осталось до следующего доклада:</b>\n"
        f"🕒 {time_delta.seconds // 3600} ч. {time_delta.seconds % 3600 // 60} мин.\n\n"
        "📊 Текущая статистика будет обновлена автоматически."
    )

    await setup_chat_action(message)
    await message.answer(response, parse_mode="HTML")


@router.message(Command("echo"))
async def echo_cmd(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        return
    if str(message.from_user.id) != os.getenv("ADMIN_ID"):
        return

    full_text = message.text or message.caption or ""
    
    command_length = len("/echo")
    text_to_send = full_text[command_length:].strip()
    
    if not text_to_send:
        await message.answer("Неправильный формат команды. Используйте /echo <текст сообщения>")
        return

    try:
        chat_id = int(os.getenv("CHAT_ID"))
        
        await message.bot.send_message(
            chat_id=chat_id,
            text=text_to_send,
            entities=message.entities[1:] if message.entities else None,
            parse_mode=None
        )
        await message.answer("Сообщение успешно отправлено!")

    except ValueError:
        await message.answer("ID чата должен быть числом!")
    except Exception as e:
        await message.answer(f"Ошибка при отправке: {str(e)}")


@router.message()
async def echo_handler(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        return

    await setup_chat_action(message)

    quotes = [
        "Война — это мир. Свобода — это рабство. Незнание — сила.",
        "Кто управляет прошлым, тот управляет будущим. Кто управляет настоящим, тот управляет прошлым.",
        "Если ты хочешь представить себе будущее, представь сапог, топчущий человеческое лицо — вечно.",
        "Мы знаем, что никто не захватывает власть с намерением отказаться от неё.",
        "Не человек управляет государством, а государство управляет человеком.",
        "Правда — это то, что говорит <b>Партия</b>.",
        "<b>Старший Брат наблюдает за тобой.</b> Всегда.",
        "Мы раздавим вас в порошок.",
        "Мы не просто уничтожаем наших врагов — мы меняем их.",
        "Двоемыслие означает способность одновременно верить в две противоречащие друг другу доктрины.",
        "Пролетарии и животные свободны.",
        "Мы <b>контролируем жизнь</b> на всех её уровнях.",
        "Реальность существует в человеческом сознании и нигде больше.",
    ]

    try:
        random_quote = random.choice(quotes)
        response = (
            "📢 <b>Старший Брат напоминает:</b>\n"
            f"<i>{random_quote}</i>"
        )
        await message.answer(response, parse_mode="HTML")
    except Exception:
        response = (
            "⚠️ <b>ТРЕВОГА!</b> ⚠️\n\n"
            "🛑 Обнаружена попытка нарушения протокола!\n"
            "👁 Старший Брат расследует инцидент..."
        )
        await message.answer(response, parse_mode="HTML")
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ChatAction, ChatType

import random
import asyncio

from services.github_service import get_team_commits

router = Router()
timer = 20
async def setup_chat_action(message: Message, action: ChatAction=ChatAction.TYPING, duration: float=0.8):
    await message.bot.send_chat_action(chat_id=message.chat.id, action=action)
    await asyncio.sleep(duration)


async def send_stats(message: Message):
    global timer

    while True:
        if timer > 0:
            await asyncio.sleep(1)
            timer -= 1
        else:
            timer = 3600
            REPOSITORIES = [
                {"owner": "AlexMarchu", "name": "tpshbot"}
            ]

            team_commits = await get_team_commits(REPOSITORIES)
            if team_commits:
                response = "*Отчет о продуктивности за последний час:*\n"
                for repo_name, count in team_commits.items():
                    response += f"• 📦 {repo_name}: {count} коммитов\n"
                response += (
                    "\nСтарший Брат одобряет вашу продуктивность.\n"
                    "Продолжайте в том же духе, товарищи.\n"
                    "Достойный труд будет вознагражден."
                )
            else:
                response = (
                    "🛑 За последний час коммитов не было. 🛑\n"
                    "Старший Брат недоволен вашей бездеятельностью.\n"
                    "Помните: безделье — это преступление.\n"
                    "🕵️‍♂️ Министерство любви уже в курсе."
                )

            await message.answer(response)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await setup_chat_action(message)
    asyncio.create_task(send_stats(message))
    response = (
        f"Добро пожаловать, товарищ {message.from_user.full_name}.\n"
        "Старший Брат наблюдает за тобой.🪖\n"
        "Война — это мир. Свобода — это рабство. Незнание — сила.\n"
        "Сообщите о всех подозрительных действиях.🚨"
    )
    await message.answer(response)


@router.message(Command("stats"))
async def cmd_stats(message: Message):

    minutes_left = int(timer // 60)
    seconds_left = int(timer % 60)
    response = (
        f"⏳ *Осталось до следующего доклада:*\n"
        f"🕒 {minutes_left} мин. {seconds_left} сек.\n\n"
        f"📊 Текущая статистика будет обновлена автоматически."
    )

    await setup_chat_action(message)
    await message.answer(response)


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
        "Правда — это то, что говорит *Партия*.",
        "*Старший Брат наблюдает за тобой.* Всегда.",
        "Мы раздавим вас в порошок.",
        "Мы не просто уничтожаем наших врагов — мы меняем их.",
        "Двоемыслие означает способность одновременно верить в две противоречащие друг другу доктрины.",
        "Пролетарии и животные свободны.",
        "Мы *контролируем жизнь* на всех её уровнях.",
        "Реальность существует в человеческом сознании и нигде больше.",
    ]
    
    try:
        random_quote = random.choice(quotes)
        response = (
            f"📢 *Старший Брат напоминает:*\n"
            f"_{random_quote}_"
        )
        await message.answer(response)
    except Exception:
        response = (
            "⚠️ *ТРЕВОГА!* ⚠️\n\n"
            "🛑 Обнаружена попытка нарушения протокола!\n"
            "👁 Старший Брат расследует инцидент..."
        )
        await message.answer(response)

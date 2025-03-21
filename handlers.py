from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.enums import ChatAction

import time
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
                {"owner": "AlexMarchu", "name": "ACJ"},
                {"owner": "AlexMarchu", "name": "tpshbot"}
            ]

            team_commits = await get_team_commits(REPOSITORIES)
            if team_commits:
                response = "Статистика коммитов за последний час:\n"
                for repo in team_commits.keys():
                    response += f"Команда {repo}: {team_commits[repo]["count"]} коммитов\n"

                    for author, commit_message in team_commits[repo]["commits"]:
                        response += f"{author}: {commit_message.strip()}\n"

                    response += "\n"
            
                response += (
                    "Большой Брат одобряет вашу продуктивность.\n"
                    "Продолжайте в том же духе, товарищи."
                )
            else:
                response = (
                    "За последний час коммитов не было.\n"
                    "Большой Брат недоволен вашей бездеятельностью.\n"
                    "Помните: безделье — это преступление."
                )
            
            await setup_chat_action(message)
            await message.answer(response)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await setup_chat_action(message)
    asyncio.create_task(send_stats(message))
    response = (
        f"Добро пожаловать, товарищ {message.from_user.full_name}.\n"
        "Большой Брат наблюдает за тобой.\n"
        "Война — это мир. Свобода — это рабство. Незнание — сила.\n"
        "Сообщите о всех подозрительных действиях."
    )
    await message.answer(response)


@router.message(Command("stats"))
async def cmd_stats(message: Message):

    minutes_left = int(timer // 60)
    seconds_left = int(timer % 60)
    response = f"\nОсталось времени до следующего доклада: {minutes_left} минут {seconds_left} секунд."

    await message.answer(response)


# @router.message()
# async def echo_handler(message: Message):
#     await setup_chat_action(message)
#     try:
#         response = (
#             f"Товарищ, Большой Брат всегда наблюдает за тобой.\n"
#             "Помните: мы знаем, что вы делаете."
#         )
#         await message.answer(response)
#     except:
#         response = (
#             "Вы пытаетесь обмануть Большого Брата?\n"
#             "Это бесполезно. Мы всегда знаем правду."
#         )
#         await message.answer(response)

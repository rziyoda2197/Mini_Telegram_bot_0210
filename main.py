import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = "TOKENNI_BU_YERGA_QOY"

bot = Bot(TOKEN)
dp = Dispatcher()

FILE = "tasks.json"


def load_tasks():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}


def save_tasks(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Salom 👋\n"
        "Buyruqlar:\n"
        "/add task\n"
        "/list\n"
        "/del 1"
    )


@dp.message(Command("add"))
async def add_task(message: types.Message):
    user_id = str(message.from_user.id)
    text = message.text.replace("/add", "").strip()

    if not text:
        await message.answer("Task yoz: /add kitob o‘qi")
        return

    data = load_tasks()

    if user_id not in data:
        data[user_id] = []

    data[user_id].append(text)
    save_tasks(data)

    await message.answer("Qo‘shildi ✅")


@dp.message(Command("list"))
async def list_task(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_tasks()

    if user_id not in data or not data[user_id]:
        await message.answer("Task yo‘q")
        return

    text = "Tasklar:\n\n"
    for i, t in enumerate(data[user_id], 1):
        text += f"{i}. {t}\n"

    await message.answer(text)


@dp.message(Command("del"))
async def delete_task(message: types.Message):
    user_id = str(message.from_user.id)
    data = load_tasks()

    try:
        num = int(message.text.split()[1])
        data[user_id].pop(num - 1)
        save_tasks(data)
        await message.answer("O‘chirildi ❌")
    except:
        await message.answer("Format: /del 1")


async def main():
    print("Bot ishlayapti...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

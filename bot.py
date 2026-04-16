from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "YOUR_BOT_TOKEN"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Track user progress in memory (replace with DB for production)
user_progress = {}

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("🔗 Group 1", callback_data="group1"),
        types.InlineKeyboardButton("🔗 Group 2", callback_data="group2")
    )
    keyboard.add(
        types.InlineKeyboardButton("🔒 Final Link (Locked)", callback_data="locked")
    )
    await message.answer("👋 Welcome! Join both groups to unlock the final link.", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data in ["group1", "group2"])
async def process_group_click(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if user_id not in user_progress:
        user_progress[user_id] = {"group1": False, "group2": False}

    user_progress[user_id][callback_query.data] = True

    # If both groups clicked → unlock final link
    if all(user_progress[user_id].values()):
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton("🔗 Group 1", url="https://t.me/group1"),
            types.InlineKeyboardButton("🔗 Group 2", url="https://t.me/group2")
        )
        keyboard.add(
            types.InlineKeyboardButton("✅ Final Link", url="https://example.com")
        )
        await callback_query.message.edit_text("🎉 You unlocked the final link!", reply_markup=keyboard)

    await callback_query.answer("Recorded!")

if name == "__main__":
    executor.start_polling(dp, skip_updates=True)
import logging
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, get_channel
from admin import handle_admin_commands, handle_photo, is_admin

# Loglash
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# To‘lov tugmasi
def payment_keyboard():
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("To‘lov qilish", callback_data="pay")
    )

# START komandasi
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    kanal = get_channel()
    if not kanal:
        await message.answer("Hali kanal belgilanmagan.")
        return
    text = f"To‘liq ma’lumotni quyidagi havola orqali olishingiz mumkin:\n{kanal}\n\n" \
           "To‘lov qilish uchun tugmani bosing va chekni yuboring."
    await message.answer(text, reply_markup=payment_keyboard())

# To‘lov tugmasi bosilganda
@dp.callback_query_handler(lambda c: c.data == "pay")
async def handle_pay(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.answer("To‘lovni amalga oshiring va chekni rasm sifatida yuboring.")

# Foydalanuvchi chek (rasm) yuborganda
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_user_photo(message: types.Message):
    if is_admin(message.from_user.id):
        return
    for admin_id in is_admin.admins:
        caption = f"Yangi to‘lov cheki!\nUser: {message.from_user.full_name} ({message.from_user.id})"
        keyboard = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton("1 oy", callback_data=f"approve_1_{message.from_user.id}"),
            InlineKeyboardButton("3 oy", callback_data=f"approve_3_{message.from_user.id}"),
            InlineKeyboardButton("6 oy", callback_data=f"approve_6_{message.from_user.id}")
        )
        await bot.send_photo(admin_id, message.photo[-1].file_id, caption=caption, reply_markup=keyboard)
        await message.reply("Chek muvaffaqiyatli yuborildi. Admin tasdiqlashini kuting.")

# Join so‘rovi (kanalga kirish) kuzatuv
@dp.chat_join_request_handler()
async def handle_join_request(update: types.ChatJoinRequest):
    try:
        await bot.send_message(update.from_user.id,
                               "Siz VIP kanalga kirish so‘rovini yubordingiz.\n"
                               "To‘liq ma’lumot uchun /start ni yuboring.")
    except Exception as e:
        logging.warning(f"Habar yuborib bo‘lmadi: {e}")

# Admin tugma bosganida (1/3/6 oy)
@dp.callback_query_handler(lambda c: c.data.startswith("approve_"))
async def approve_subscription(call: types.CallbackQuery):
    _, oy, user_id = call.data.split("_")
    oy = int(oy)
    user_id = int(user_id)

    duration_days = {1: 30, 3: 90, 6: 180}[oy]
    end_date = (call.message.date + types.timedelta(days=duration_days)).strftime("%Y-%m-%d")

    # Bazaga yozish
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS subscriptions (
        user_id INTEGER,
        duration INTEGER,
        end_date TEXT
    )""")
    cur.execute("INSERT INTO subscriptions VALUES (?, ?, ?)", (user_id, oy, end_date))
    con.commit()
    con.close()

    kanal = get_channel().replace("https://t.me/", "")
    try:
        await bot.approve_chat_join_request(chat_id=kanal, user_id=user_id)
        await call.message.edit_caption(call.message.caption + f"\n✅ {oy} oylik obuna tasdiqlandi.")
    except Exception as e:
        await call.message.answer(f"Qo‘shib bo‘lmadi: {e}")

# Admin buyruqlarini ulash
@dp.message_handler()
async def handle_all(message: types.Message):
    await handle_admin_commands(message)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
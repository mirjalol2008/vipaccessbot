from aiogram import types, Dispatcher from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup import sqlite3, datetime from config import ADMINS, db_path, get_channel, set_channel

admin_states = {}

Admin panelga kirish

def admin_panel(): buttons = [[InlineKeyboardButton("📢 Kanalni sozlash", callback_data="set_channel")], [InlineKeyboardButton("❌ Paneldan chiqish", callback_data="exit")]] return InlineKeyboardMarkup(inline_keyboard=buttons)

Muddat tugmachalari

def create_duration_keyboard(user_id, chat_join_request): buttons = [ [InlineKeyboardButton("1 oy", callback_data=f"approve:{user_id}:30")], [InlineKeyboardButton("3 oy", callback_data=f"approve:{user_id}:90")], [InlineKeyboardButton("6 oy", callback_data=f"approve:{user_id}:180")] ] return InlineKeyboardMarkup(inline_keyboard=buttons)

Admin buyrug'i

dp: Dispatcher = None

def setup_admin_routes(dispatcher: Dispatcher): global dp dp = dispatcher

@dp.message_handler(commands=['admin'])
async def admin_command(msg: types.Message):
    if msg.from_user.id in ADMINS:
        admin_states[msg.from_user.id] = 'panel'
        await msg.answer("Admin panelga xush kelibsiz", reply_markup=admin_panel())

@dp.callback_query_handler(lambda c: c.data == 'set_channel')
async def set_channel_prompt(call: types.CallbackQuery):
    admin_states[call.from_user.id] = 'awaiting_channel'
    await call.message.edit_text("Yangi kanal havolasini yuboring: (masalan, t.me/vipkanal)")

@dp.message_handler(lambda msg: admin_states.get(msg.from_user.id) == 'awaiting_channel')
async def receive_channel(msg: types.Message):
    if msg.text.startswith("t.me/"):
        set_channel(msg.text.strip())
        admin_states[msg.from_user.id] = 'panel'
        await msg.answer("✅ Kanal muvaffaqiyatli belgilandi", reply_markup=admin_panel())
    else:
        await msg.answer("Iltimos, to'g'ri kanal havolasini yuboring (t.me/...) ")

@dp.callback_query_handler(lambda c: c.data == 'exit')
async def exit_panel(call: types.CallbackQuery):
    admin_states.pop(call.from_user.id, None)
    await call.message.edit_text("Admin paneldan chiqdingiz")

@dp.callback_query_handler(lambda c: c.data.startswith("approve:"))
async def approve_user(call: types.CallbackQuery):
    _, user_id, days = call.data.split(":")
    user_id = int(user_id)
    duration = int(days)
    now = datetime.datetime.now()
    end_date = now + datetime.timedelta(days=duration)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id INTEGER,
            duration INTEGER,
            end_date TEXT
        )
    """)
    cur.execute("REPLACE INTO subscriptions (user_id, duration, end_date) VALUES (?, ?, ?)",
                (user_id, duration, end_date.isoformat()))
    conn.commit()
    conn.close()

    # VIP kanalga qo'shish
    channel = get_channel()
    try:
        await dp.bot.approve_chat_join_request(chat_id=channel, user_id=user_id)
        await call.message.answer(f"✅ {duration} kunlik obuna tasdiqlandi va foydalanuvchi kanalga qo'shildi")
        await dp.bot.send_message(user_id, f"Siz {duration} kunlik VIP obunaga qabul qilindingiz. Muddati: {end_date.strftime('%Y-%m-%d %H:%M')}")
    except Exception as e:
        await call.message.answer(f"Xatolik: {e}")


# vipaccessbot
# VIP Access Bot

Telegram bot for managing paid access to a VIP channel.

## Features
- Auto-monitor join requests (no need for user to press /start)
- Sends instructions + payment button
- Admin panel to set channel and card number
- Admin approves check manually (1/3/6 month access)
- Auto save to SQLite
- Auto-kick when subscription ends

## Setup

```bash
git clone https://github.com/mirjalol2008/vipaccessbot
cd vipaccessbot
pip install -r requirements.txt

Update your config.py:

BOT_TOKEN = "your_telegram_bot_token"
ADMIN_ID = 123456789



Run the bot:

python bot.py


Admin Commands

/admin — Open admin panel

/setchannel t.me/YourChannel — Set VIP channel link

/exit — Exit admin mode


License

MIT License - see LICENSE file

See CONTRIBUTING.md for how to contribute.

---
 CREATE BY😎 mirjalol2008

# vipaccessbot
# VIP Access Bot

Telegram bot that monitors join requests to a private VIP channel and handles automated payments and subscriptions.

## Features
- Auto-detect join requests
- Sends instruction message even if user hasn't pressed `/start`
- Admin panel with `/admin` access
- Set channel with `/setchannel <link>`
- Payment button and manual check image upload
- Admin approves with 1/3/6 month option
- Stores subscription in SQLite and auto-kicks after expiry

## Setup

1. Clone the repository:
```bash
git clone https://github.com/mirjalol2008/vipaccessbot
cd vipaccessbot

Install dependencies:
pip install -r requirements.txt

Configure your bot token: Edit config.py and paste your Bot Token:
BOT_TOKEN = "YOUR_BOT_TOKEN"

Run the bot:
python bot.py

Admin Commands

/admin — Open admin panel

/setchannel t.me/YourChannelLink — Set VIP channel

/exit — Exit admin panel

database.db and channel.txt are generated automatically.

Auto-kick will be handled based on saved subscription duration.



---

Made with ❤️ by mirjalol2008

---

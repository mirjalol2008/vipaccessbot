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

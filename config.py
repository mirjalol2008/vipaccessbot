BOT_TOKEN = "bot_tokenni_bu_yerga_joylang"

# Kanal havolasini saqlash uchun oddiy faylga yozish/oqish funksiyalari
import os

CHANNEL_FILE = "channel.txt"

def get_channel():
    if os.path.exists(CHANNEL_FILE):
        with open(CHANNEL_FILE, "r") as f:
            return f.read().strip()
    return ""

def set_channel(link):
    with open(CHANNEL_FILE, "w") as f:
        f.write(link)
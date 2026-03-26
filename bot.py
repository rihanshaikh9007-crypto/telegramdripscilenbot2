import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8479108013:AAGa93idRH2u5TTcWDt2DPAvihdi2XxDhN0"
ADMIN_ID = 1484173564

channels = []   # dynamic channels list
user_state = {}

# 🔑 Key generator
def generate_key():
    return ''.join(random.choices(string.digits, k=10))

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []

    for i, ch in enumerate(channels):
        keyboard.append([InlineKeyboardButton(f"Join Channel {i+1} 🔥", url=ch["link"])])

    keyboard.append([InlineKeyboardButton("✅ VERIFY", callback_data="verify")])

    text = """👻 Sab channels join karo phir VERIFY dabao

𝗛ᴇʟʟᴏ 𝗨ꜱᴇʀ 👻 𝐁𝐎𝐓

ALL CHANNEL JOIN 🥰

𝐇𝐎𝐖 𝐓𝐎 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐄 𝐊𝐄𝐘 💀
CLICK HERE"""

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# VERIFY
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    for ch in channels:
        try:
            member = await context.bot.get_chat_member(ch["id"], user_id)
            if member.status not in ["member", "administrator", "creator"]:
                await query.answer()
                await query.message.reply_text(f"❌ Pehle join karo: {ch['name']}")
                return
        except:
            await query.answer()
            await query.message.reply_text("❌ Error checking channels")
            return

    key = generate_key()

    await query.message.reply_text(
        f"Key - {key}\n\n"
        "DRIP SCINET APK - https://www.mediafire.com/file/if3uvvwjbj87lo2/DRIPCLIENT_v6.2_GLOBAL_AP.apks/file"
    )

# ADMIN PANEL
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    keyboard = [
        [InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")]
    ]

    await update.message.reply_text("Admin Panel ⚙️", reply_markup=InlineKeyboardMarkup(keyboard))

# Button click
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        return

    if query.data == "add_channel":
        user_state[user_id] = "waiting_channel"
        await query.message.reply_text("Channel ID aur invite link bhejo\n\nFormat:\n-100xxxx https://t.me/+link")

    elif query.data == "verify":
        await verify(update, context)

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id == ADMIN_ID and user_state.get(user_id) == "waiting_channel":
        try:
            parts = update.message.text.split()
            channel_id = int(parts[0])
            link = parts[1]

            member = await context.bot.get_chat_member(channel_id, context.bot.id)

            if member.status in ["administrator", "creator"]:
                channels.append({
                    "id": channel_id,
                    "link": link,
                    "name": f"Channel {len(channels)+1}"
                })

                await update.message.reply_text("✅ Channel added successfully")
                user_state[user_id] = None
            else:
                await update.message.reply_text("❌ Bot admin nahi hai channel me")

        except:
            await update.message.reply_text("❌ Format galat hai")

# MAIN
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()

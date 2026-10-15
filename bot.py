import os
import telebot
import requests

# --------------------- CONFIG (Railway Variables se aayega) ---------------------
API_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
FORCE_JOIN_CHANNEL = os.getenv("FORCE_JOIN_CHANNEL", "-1003023135446")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/ll_ABOUT_SASUKE_ll")
BUTTON_NAME = os.getenv("BUTTON_NAME", "Channel")
LIKE_API_URL = os.getenv("LIKE_API_URL")  # e.g. http://IP:5002/like

if not API_TOKEN:
    raise SystemExit("BOT_TOKEN variable set nahi hai!")

bot = telebot.TeleBot(API_TOKEN)

# --------------------- HELPERS ---------------------
def is_user_member(user_id):
    if user_id == OWNER_ID:
        return True
    try:
        member = bot.get_chat_member(FORCE_JOIN_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False


def join_markup(verify_text="✅ VERIFY"):
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton(f"🔗 JOIN {BUTTON_NAME}", url=CHANNEL_LINK),
        telebot.types.InlineKeyboardButton(verify_text, callback_data="verify_membership"),
    )
    return markup


def send_join_required(message):
    bot.reply_to(
        message,
        "🚫 Aᴄᴄᴇss Dᴇɴɪᴇᴅ!\n\n"
        "Yᴏᴜ Mᴜsᴛ Jᴏɪɴ Oᴜʀ Oғғɪᴄɪᴀʟ Cʜᴀɴɴᴇʟ Fɪʀsᴛ Tᴏ Usᴇ Tʜɪs Bᴏᴛ.\n\n"
        f"📢 Cʜᴀɴɴᴇʟ: {CHANNEL_LINK}\n\n"
        "✅ Aғᴛᴇʀ Jᴏɪɴɪɴɢ, Tᴀᴘ Tʜᴇ *Vᴇʀɪғʏ* Bᴜᴛᴛᴏɴ Bᴇʟᴏᴡ.",
        parse_mode="Markdown",
        reply_markup=join_markup(),
    )


USAGE_TEXT = (
    "✅ *Rᴇᴀᴅʏ Tᴏ Usᴇ!*\n\n"
    "🎮 *Usᴀɢᴇ:*\n"
    "`/like ind 1055975097`\n\n"
    "🌍 *Sᴜᴘᴘᴏʀᴛᴇᴅ Rᴇɢɪᴏɴs:*\n"
    "• 🇮🇳 `ind` → Iɴᴅɪᴀ\n"
    "• 🇮🇩 `id` → Iɴᴅᴏɴᴇsɪᴀ\n"
    "• 🇸🇬 `sg` → Sɪɴɢᴀᴘᴏʀᴇ\n"
    "• 🇲🇾 `my` → Mᴀʟᴀʏsɪᴀ\n"
    "• 🇵🇭 `ph` → Pʜɪʟɪᴘᴘɪɴᴇs\n\n"
    "💡 *Exᴀᴍᴘʟᴇ:*\n"
    "`/like sg 1234567890`"
)

# --------------------- HANDLERS ---------------------
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id

    if user_id == OWNER_ID:
        bot.reply_to(
            message,
            "👑 Wᴇʟᴄᴏᴍᴇ Mᴀsᴛᴇʀ!\n\n"
            "✅ Uɴʟɪᴍɪᴛᴇᴅ Aᴄᴄᴇss Aᴄᴛɪᴠᴇ\n"
            "✅ Fᴏʀᴄᴇ Jᴏɪɴ Dɪsᴀʙʟᴇᴅ\n\n"
            "🎮 Cᴏᴍᴍᴀɴᴅ: `/like {region} {uid}`\n"
            "Exᴀᴍᴘʟᴇ: `/like ind 1055975097`",
            parse_mode="Markdown",
        )
        return

    if not is_user_member(user_id):
        send_join_required(message)
        return

    bot.reply_to(message, USAGE_TEXT, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == "verify_membership")
def handle_verify(call):
    if is_user_member(call.from_user.id):
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🚀 START USING BOT", callback_data="start_using"))
        bot.edit_message_text(
            "✅ Vᴇʀɪғɪᴄᴀᴛɪᴏɴ Sᴜᴄᴄᴇssғᴜʟ!\n\nCʟɪᴄᴋ ʙᴇʟᴏᴡ ᴛᴏ sᴛᴀʀᴛ 👇",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup,
        )
        bot.answer_callback_query(call.id, "✅ Verified!")
    else:
        bot.edit_message_text(
            "🚫 Yᴏᴜ Hᴀᴠᴇɴ'ᴛ Jᴏɪɴᴇᴅ Yᴇᴛ.\n\n"
            f"📢 Pʟᴇᴀsᴇ Jᴏɪɴ Fɪʀsᴛ: {CHANNEL_LINK}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=join_markup("✅ VERIFY AGAIN"),
        )
        bot.answer_callback_query(call.id, "❌ Please join the channel first!")


@bot.callback_query_handler(func=lambda call: call.data == "start_using")
def handle_start_using(call):
    bot.edit_message_text(
        USAGE_TEXT,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown",
    )
    bot.answer_callback_query(call.id, "🎉 Bot is ready to use!")


@bot.message_handler(commands=["like"])
def handle_like(message):
    user_id = message.from_user.id

    if not is_user_member(user_id):
        send_join_required(message)
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(
            message,
            "❌ Usᴀɢᴇ: `/like {region} {uid}`\nExᴀᴍᴘʟᴇ: `/like ind 1055975097`",
            parse_mode="Markdown",
        )
        return

    region, uid = args[1], args[2]

    wait_text = "👑 Pʀᴏᴄᴇssɪɴɢ Oᴡɴᴇʀ Rᴇǫᴜᴇsᴛ..." if user_id == OWNER_ID else "⏳ Pʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ..."
    sent_msg = bot.reply_to(message, wait_text)

    if not LIKE_API_URL:
        bot.edit_message_text("❌ LIKE_API_URL set nahi hai.", chat_id=message.chat.id, message_id=sent_msg.message_id)
        return

    try:
        response = requests.get(LIKE_API_URL, params={"uid": uid, "server_name": region}, timeout=30)
        data = response.json()

        name = data.get("PlayerNickname", "N/A")
        likes_before = data.get("LikesbeforeCommand", "0")
        likes_given = data.get("LikesGivenByAPI", "0")
        likes_after = data.get("LikesafterCommand", "0")
        remaining = "♾️ UNLIMITED" if user_id == OWNER_ID else data.get("remains", "N/A")

        text = (
            "🎉 Lɪᴋᴇ Sᴜᴄᴄᴇssғᴜʟʟʏ 👍\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"👑 Nᴀᴍᴇ: {name}\n"
            f"🕹️ Uɪᴅ: {uid}\n"
            f"🌐 Rᴇɢɪᴏɴ: {region.upper()}\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"❤️ Lɪᴋᴇs Bᴇғᴏʀᴇ: {likes_before}\n"
            f"🩵 Lɪᴋᴇs Gɪᴠᴇɴ: {likes_given}\n"
            f"💚 Lɪᴋᴇs Aғᴛᴇʀ: {likes_after}\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 Rᴇᴍᴀɪɴɪɴɢ: {remaining}"
        )
        if user_id == OWNER_ID:
            text += "\n━━━━━━━━━━━━━━━━━━━━━\n👑 OWNER UNLIMITED ACCESS 👑"

        bot.edit_message_text(text, chat_id=message.chat.id, message_id=sent_msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ Eʀʀᴏʀ Cᴏɴɴᴇᴄᴛɪᴏɴ ᴛᴏ API\n{e}",
            chat_id=message.chat.id,
            message_id=sent_msg.message_id,
        )


# --------------------- START ---------------------
if __name__ == "__main__":
    print("🤖 LIKE BOT IS RUNNING")
    try:
        if OWNER_ID:
            bot.send_message(OWNER_ID, "🤖 LIKE BOT IS RUNNING 🏃")
    except Exception as e:
        print(f"Owner ko startup message nahi gaya: {e}")

    bot.infinity_polling(skip_pending=True)

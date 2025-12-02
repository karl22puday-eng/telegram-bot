import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters


PASSWORD = "Caviar$"  # <-- Change this to your password
ALLOWED_USERS_FILE = "allowed_users.txt"

# Load allowed users from file
if os.path.exists(ALLOWED_USERS_FILE):
    with open(ALLOWED_USERS_FILE, "r") as f:
        ALLOWED_USERS = {int(line.strip()) for line in f.readlines()}
else:
    ALLOWED_USERS = set()


async def start(update, context):
    user_id = update.effective_user.id

    # Already authorized
    if user_id in ALLOWED_USERS:
        await update.message.reply_text("✅ You are already authorized!")
        return

    await update.message.reply_text("🔒 This bot is protected.\nPlease enter the password:")
    context.user_data["awaiting_password"] = True


async def handle_message(update, context):
    user_id = update.effective_user.id
    text = update.message.text

    # If awaiting password
    if context.user_data.get("awaiting_password"):
        if text == PASSWORD:
            ALLOWED_USERS.add(user_id)
            with open(ALLOWED_USERS_FILE, "a") as f:
                f.write(str(user_id) + "\n")

            context.user_data["awaiting_password"] = False
            await update.message.reply_text("🎉 Access granted! Welcome!")
        else:
            await update.message.reply_text("❌ Wrong password. Try again.")
        return

    # If user is NOT authorized
    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("⛔ You are not authorized.\nUse /start to try again.")
        return

    # Normal bot behavior for authorized users
    await update.message.reply_text(f"You said: {text}")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()


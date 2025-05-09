# 引入所需的库
import os
from dotenv import load_dotenv
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
# 加载 .env 文件
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
RAILWAY_URL = os.getenv("RAILWAY_URL")

# 加载需要引用的文件
from handlers.command_handlers import start,cx1, lm1, help
from handlers.callback_handlers import button_handler
from handlers.reply_handlers import handle_reply_message

# 设置命令菜单，当用户在 Telegram 对话框中输入 / 时，会显示可用的命令菜单。
async def set_commands(app):
    commands = [
        BotCommand("start", "开始"),
        BotCommand("cx1", "综合查询（1积分）"),
        BotCommand("lm1", "猎魔（3积分）"),
        BotCommand("help", "使用说明")
    ]
    await app.bot.set_my_commands(commands)

# Start函数，初始化和启动整个 Telegram Bot
def main():
    # 构建一个Bot实例，使用提供的TOKEN
    app = ApplicationBuilder().token(TOKEN).build()
    # 设置命令菜单
    app.post_init = set_commands

    # 处理用户发送指令时调用的函数。
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cx1", cx1))
    app.add_handler(CommandHandler("lm1", lm1))
    app.add_handler(CommandHandler("help", help))

    # 处理按钮点击回调（InlineKeyboard）时调用的 button_handler 函数。
    app.add_handler(CallbackQueryHandler(button_handler))
    # 处理用户发送的消息时调用的函数。
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, handle_reply_message))

    # ⚠️ 使用 Railway 的 URL（必须是 HTTPS）并追加 webhook 路径
    webhook_path = "/telegram-webhook"
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        webhook_url=f"{RAILWAY_URL}{webhook_path}"
    )

# 确保这段脚本作为“主程序”执行时才会运行 main()，而不是被别的模块导入时执行。
if __name__ == '__main__':
    main()
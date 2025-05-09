# 引入所需的库
from telegram import Update
from telegram.ext import ContextTypes

# 加载需要引用的文件
from handlers.command_handlers import cx1, lm1

async def handle_reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 如果不是回复，就跳过
    if not update.message or not update.message.reply_to_message:
        return

    reply_text = update.message.reply_to_message.text or ""

    # 判断回复的是哪个命令的提示文字
    if "（姓名/身份证/手机号）" in reply_text:
    # 把用户的输入当作 /cx1 参数处理
        context.args = [update.message.text.strip()]
        await cx1(update, context)
    elif "（姓名+地区+性别+起始年龄+结束年龄）" in reply_text:
        context.args = update.message.text.strip().split()
        await lm1(update, context)
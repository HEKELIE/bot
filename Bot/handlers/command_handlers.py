# 引入所需的库
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.query_helper import handle_query

# 加载text文本文件
from text import ZHCX_TEXT, LM_TEXT, HELP_TEXT
from utils.query_helper import lm1_validator, send_reply

# /start指令 主菜单
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("查询命令", callback_data='find_command'),
            InlineKeyboardButton("使用说明", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("你好，请选择一个操作：", reply_markup=reply_markup)
    else:
        # 如果是回调查询，则使用 edit_message_text
        await update.callback_query.edit_message_text("你好，请选择一个操作：", reply_markup=reply_markup)

# /cx1 命令处理函数：综合查询（如：姓名、身份证、手机号）
async def cx1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_query(
        update,                     # Telegram 消息对象（可能来自用户消息或按钮回调）
        context,                    # 上下文对象，包含用户输入的命令参数
        ZHCX_TEXT,              # 没有参数时发送的帮助文本（从 text.py 导入）
        "❌ 综合查询参数格式错误\n请使用：姓名/身份证/手机号\n\n如果您需要帮助，请输入 /help 获取更多信息。",   # 参数格式错误时发送的提示语
        1,                          # 期望参数数量：1 个（如姓名、身份证号等）
        lambda args: args[0]        # 格式化函数：直接返回第一个参数作为查询值
    )

# /lm1 命令处理函数：猎魔查询（如：姓名 + 地区 + 性别 + 起始年龄 + 结束年龄）
async def lm1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if args and not lm1_validator(args):
        await send_reply(update, "❌ 猎魔参数格式错误\n请使用：姓名 地区 性别 起始年龄 结束年龄\n\n注意:\n1.性别为“男/女”\n2.年龄为数字，且起始年龄 ≤ 结束年龄。\n\n如果您需要帮助，请输入 /help 获取更多信息。")
        return

    await handle_query(
        update,                             # Telegram 消息对象
        context,                            # 上下文对象
        LM_TEXT,                        # 没有参数时发送的帮助文本
        "❌ 猎魔参数格式错误\n请使用：姓名 地区 性别 起始年龄 结束年龄\n\n如果您需要帮助，请输入 /help 获取更多信息。",  # 参数格式错误提示语
        5,                                  # 期望参数数量：5 个
        lambda args: " ".join(args),         # 格式化函数：将 5 个参数拼接成一个字符串
    )

# /help命令处理
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
    [InlineKeyboardButton("返回主菜单", callback_data='back_start')]
]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(HELP_TEXT, reply_markup=reply_markup)
    else:
        # 如果是回调查询，则使用 edit_message_text
        await update.callback_query.edit_message_text(HELP_TEXT, reply_markup=reply_markup)
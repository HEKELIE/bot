# 引入所需的库
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# 加载需要引用的文件
from handlers.command_handlers import start, cx1, lm1
from handlers.command_handlers import help

# ------------------------------------------------------------------------------------------------------------------------
# 按钮统一处理函数 button_handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): # 用于处理所有回调按钮（CallbackQuery）事件
    query = update.callback_query # 从更新对象中获取回调查询（CallbackQuery）对象
    data = query.data # 获取用户点击按钮时附带的回调数据（callback_data）
    await query.answer() # 对回调进行快速响应，防止 Telegram 客户端超时（必须调用）

    # 判断回调数据，执行相应的操作
    # ------------------------------------------------------------
    # 处理查询命令按钮
    if data == 'find_command':
        await find_menu(update, context)
    # ------------------------------------------------------------
    # 处理查询选项按钮
    # 综合查询
    elif data == 'cx1':
        await cx1(update, context)
    # 猎魔查询
    elif data == 'lm1':
        await lm1(update, context)
    # ------------------------------------------------------------
    # 处理帮助按钮
    elif data == 'help':
        await help(update, context)

    # ------------------------------------------------------------
    # 通用按钮
    # 返回主菜单
    elif data == 'back_start':
        await start(update, context)
    else:
        await query.edit_message_text("未知选项")
# ------------------------------------------------------------------------------------------------------------------------


# 查询菜单函数：显示查询选项
async def find_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # 对回调进行快速响应，防止 Telegram 客户端超时（必须调用） 

    keyboard = [
    [
        InlineKeyboardButton("综合查询（1积分）", callback_data='cx1'),
        InlineKeyboardButton("猎魔（3积分）", callback_data='lm1')
    ],
    [InlineKeyboardButton("返回主菜单", callback_data='back_start')]
]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        await update.message.reply_text("你好，请选择一个操作：", reply_markup=reply_markup)
    else:
        # 如果是回调查询，则使用 edit_message_text
        await update.callback_query.edit_message_text("你好，请选择一个操作：", reply_markup=reply_markup)
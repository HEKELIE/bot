# 引入所需的库
from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from typing import Callable


# 判断是 message 还是 callback_query
async def send_reply(update: Update, text: str, force_reply: bool = False):
    if update.message:
        await update.message.reply_text(text, reply_markup=ForceReply(selective=True) if force_reply else None)
    elif update.callback_query:
        if force_reply:
            await update.callback_query.message.reply_text(text, reply_markup=ForceReply(selective=True))


# 通用处理函数：参数判断 + 格式校验 + 回复
async def handle_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    help_text: str,
    usage_text: str,
    expected_arg_count: int,
    formatter: Callable,
    command_prefix: str = ""
):
    args = context.args or []

    # 合并用户输入为一个整体并按空格检查数量
    raw_input = " ".join(args).strip()
    split_args = raw_input.split()

    # 没有参数时，发送帮助 + 弹出输入框
    if not args:
        await send_reply(update, help_text, force_reply=True)
        return
    # 正确参数数量：处理查询
    if len(split_args) == expected_arg_count:
        formatted = formatter(split_args)
        await send_reply(update, f"查询结果：{formatted}")
    # 参数数量错误：发送提示
    else:
        await send_reply(update, f"{usage_text}")

# 参数验证函数

def is_valid_gender(gender: str) -> bool:
    """判断性别是否合法（男/女）"""
    return gender in ["男", "女"]

def is_valid_age(age: str) -> bool:
    """判断是否是合法的整数年龄"""
    try:
        int(age)
        return True
    except ValueError:
        return False

def is_valid_age_range(start: str, end: str) -> bool:
    """判断年龄区间是否合法（起始 ≤ 结束）"""
    try:
        return int(start) <= int(end)
    except ValueError:
        return False

def lm1_validator(args: list) -> bool:
    """
    猎魔查询参数验证：
    [姓名, 地区, 性别, 起始年龄, 结束年龄]
    """
    if len(args) != 5:
        return False
    name, region, gender, start_age, end_age = args
    return (
        name.strip() != "" and
        region.strip() != "" and
        is_valid_gender(gender) and
        is_valid_age(start_age) and
        is_valid_age(end_age) and
        is_valid_age_range(start_age, end_age)
    )
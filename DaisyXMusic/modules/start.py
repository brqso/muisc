from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from DaisyXMusic.config import (
    BOT_USERNAME,
    PROJECT_NAME,
    SOURCE_CODE,
    SUPPORT_GROUP,
    UPDATES_CHANNEL,
)
from DaisyXMusic.modules.msg import Messages as tr


@Client.on_message(filters.private & filters.incoming & filters.command(["start"]))
def _start(client, message):
    client.send_message(
        message.chat.id,
        text=tr.START_MSG.format(message.from_user.first_name, message.from_user.id),
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ اضفني إلى مجموعتك 🙋‍♀️",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "📲 التحديثات", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                    InlineKeyboardButton(
                        "💬 جروب الدعم", url=f"https://t.me/{SUPPORT_GROUP}"
                    ),
                ],
                [InlineKeyboardButton("🛠 كود السورس 🛠", url=f"https://{SOURCE_CODE}")],
            ]
        ),
        reply_to_message_id=message.message_id,
    )


@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
    await message.reply_text(
        f"""**🔴 {PROJECT_NAME} is online**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "💬 جروب الدعم", url=f"https://t.me/{SUPPORT_GROUP}"
                    )
                ]
            ]
        ),
    )


@Client.on_message(filters.private & filters.incoming & filters.command(["help"]))
def _help(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text=tr.HELP_MSG[1],
        parse_mode="markdown",
        disable_web_page_preview=True,
        disable_notification=True,
        reply_markup=InlineKeyboardMarkup(map(1)),
        reply_to_message_id=message.message_id,
    )


help_callback_filter = filters.create(
    lambda _, __, query: query.data.startswith("help+")
)


@Client.on_callback_query(help_callback_filter)
def help_answer(client, callback_query):
    chat_id = callback_query.from_user.id
    message_id = callback_query.message.message_id
    msg = int(callback_query.data.split("+")[1])
    client.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=tr.HELP_MSG[msg],
        reply_markup=InlineKeyboardMarkup(map(msg)),
    )


def map(pos):
    if pos == 1:
        button = [[InlineKeyboardButton(text="▶️", callback_data="help+2")]]
    elif pos == len(tr.HELP_MSG) - 1:
        url = f"https://t.me/{SUPPORT_GROUP}"
        button = [
            [
                InlineKeyboardButton(
                    "➕ اضفني إلى مجموعتك🙋‍♀️",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📲 التحديثات", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
                InlineKeyboardButton(
                    text="💬 جروب الدعم", url=f"https://t.me/{SUPPORT_GROUP}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🛠 كود السورس 🛠", url=f"https://{SOURCE_CODE}"
                )
            ],
            [InlineKeyboardButton(text="◀️", callback_data=f"help+{pos-1}")],
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text="◀️", callback_data=f"help+{pos-1}"),
                InlineKeyboardButton(text="▶️", callback_data=f"help+{pos+1}"),
            ],
        ]
    return button


@Client.on_message(filters.command("help") & ~filters.private & ~filters.channel)
async def ghelp(_, message: Message):
    await message.reply_text(
        f"""**🙋‍♀️ انا بوت استطيع تشغيل الموسيقى في المجموعات او القنوات.**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🟡 اضغط هنا للمساعدة 🟡",
                        url=f"https://t.me/{BOT_USERNAME}?start",
                    )
                ]
            ]
        ),
    )

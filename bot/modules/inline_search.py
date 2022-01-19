from bot import app, LOGGER
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from pyrogram.errors import QueryIdInvalid

@app.on_inline_query()
async def inline_search(_, event: InlineQuery):
    answers = list()
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="Inline Search Mode",
                description="You can directly search for leeched files from here",
                input_message_content=InputTextMessageContent(
                    message_text="You can search for the leeched files from anywhere directly",
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Search Here", switch_inline_query_current_chat="")],
                    [InlineKeyboardButton("Mirror Group", url="https://t.me/Fubuki_mirror")]
                ])
            )
        )
    else:
        key = event.query
        gdrive = GoogleDriveHelper()
        msg, url = gdrive.drive_list(key, isRecursive=False, itemType="both", inline=True)
        if url:
            answers.append(
                InlineQueryResultArticle(
                    title=f"Found Result for {key}",
                    description="Click To Get Link",
                    input_message_content=InputTextMessageContent(
                        message_text=msg,
                        disable_web_page_preview=True
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Result", url=url)],
                        [InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")],
                    ])
                )
            )
        else:
            answers.append(
                InlineQueryResultArticle(
                    title=f"No Result Found for {key}",
                    description="Try with another search key",
                    input_message_content=InputTextMessageContent(
                        message_text=msg,
                        disable_web_page_preview=True
                    ),
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")],
                    ])
                )
            )
        try:
            await event.answer(
                results=answers,
                cache_time=0
            )
        except QueryIdInvalid:
            LOGGER.info(f"QueryIdInvalid: {event.query}")

from bot import app, LOGGER
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent
from bot.helper.mirror_utils.upload_utils.gdriveTools import GoogleDriveHelper
from pyrogram.errors import QueryIdInvalid

@app.on_inline_query()
async def inline_search(_, event: InlineQuery):
    answers = list()
    LOGGER.info(event.query)
    if event.query == "":
        LOGGER.info("Empty query")
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
                    [InlineKeyboardButton("Mirror Group", url="https://t.me/Fubuki_mirror")],
                ])
            )
        )
    else:
        key = event.query
        gdrive = GoogleDriveHelper()
        file_title, desc, drive_url, index_url, view_link = gdrive.drive_list_inline(key, isRecursive=False, itemType="both")
        if file_title:
            for title in file_title:
                answers.append(
                    InlineQueryResultArticle(
                        title=title,
                        description=desc[file_title.index(title)],
                        input_message_content=InputTextMessageContent(
                            message_text=f"Title : {title}\n{desc[file_title.index(title)]}",
                            disable_web_page_preview=True
                        ),
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("View Link", url=view_link[file_title.index(title)])],
                            [InlineKeyboardButton("Drive Link", url=drive_url[file_title.index(title)])],
                            [InlineKeyboardButton("Index Link", url=index_url[file_title.index(title)])],
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
                        message_text="No Result Found For Your Search Key\nTry with another search",
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

import html
import logging

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InaccessibleMessage
from aiogram.utils.text_decorations import html_decoration, markdown_decoration

logger = logging.getLogger(__name__)

router = Router()


async def handle_callback(callback: CallbackQuery, msg: str, parse_mode: str):
    if not isinstance(callback.message, InaccessibleMessage) and callback.message.text:
        try:
            if msg != callback.message.text:
                await callback.message.edit_text(
                    text=msg,
                    reply_markup=callback.message.reply_markup,
                    parse_mode=parse_mode,
                )
        except TelegramBadRequest as e:
            logger.error("Message not modified. Suspending.")
        await callback.answer()


# rework this part so to use html escape for comments and html_deoration methods
@router.callback_query(F.data == "html_style")
async def html_style(callback: CallbackQuery):
    description: str = html.escape(
        "Use <b>Bold text</b> or <strong></strong> to make text bold\n"
        "Use <i>Italic text</i> or <em></em> to make text italic\n"
        "Use <u>Underlined text</u> or <ins></ins> to make text underlined\n"
        "Use <s>Strikethrough text</s> optionally you can use <strike></strike> or <del></del> to make text strikethrough\n"
        'Use <span class="tg-spoiler">Text under spoiler</span> or <tg-spoiler></tg-spoiler> to make text hidden until user clicks on it\n'
        'Use <a href="https://google.com">Google link</a> to insert a link\n'
        "Use <code>Monowidth text</code> to make text monowidth\n"
        "Use <pre>Preformatted text</pre> to make text preformatted\n"
        'Use <pre><code class="language-pthon">from time import time\n'
        "print(time())</code></pre>\n"
        "Use <blockquote>Quote</blockquote> to decorate text as a quote\n"
        "Use <blockquote expandable>Quote</blockquote> to make the quote expandable\n"
        "You can also cobine modifiers. For example: <b><i>Bold and italic text</i><b>\n"
        "The convenient way to apply modifiers and avoid typos is to use html_decoration from aiogram.utils.text_decorations\n"
    )
    msg = (
        description
        + f"""
{html_decoration.bold("Bold text")}
{html_decoration.italic("Italic")}
{html_decoration.underline("Underlined")}
{html_decoration.strikethrough("strikethrough text")}
{html_decoration.spoiler("Spoiler")}
{html_decoration.link("Google link", "https://google.com")}
{html_decoration.code("Monowidth text")}
{html_decoration.pre("Preformatted text")}
{html_decoration.pre_language("if True: print('Success')", "python")}
{html_decoration.expandable_blockquote("""This is an expandeble quote.
Only beginning of the quote is visible. To see the whole quote user should click on it
Lorem ipsum dolor sit amet consectetur adipisicing elit. Cumque accusantium quos voluptas corrupti earum reprehenderit porro debitis ut labore quaerat, illum soluta vel praesentium quo commodi veniam\! Vero laborum reiciendis dicta, laudantium voluptatem eius assumenda ut modi atque ipsam neque non voluptatum! Quisquam modi, neque in porro accusamus quasi autem?""")}
{html_decoration.bold(html_decoration.underline("Bold and underlined text"))}
"""
    )

    await handle_callback(callback, msg, "HTML")


@router.callback_query(F.data == "markdown_style")
async def markdown_style(callback: CallbackQuery):
    description: str = (
        r"Use \*Bold text\*  to make text bold\n"
        r"Use \_Italic text\_ to make text italic\n"
        r"Use __Underlined text__ to make text underlined\n"
        r"Use \~Strikethrough text\~ to make text strikethrough\n"
        r"Use \|\|Text under spoiler\|\| to make text hidden until user clicks on it\n"
        r"Use \[Google Link\]\(https://google\.com\) to insert a link\n"
        r"Use \`Monowidth text\` to make text monowidth\n"
        r"Use \`\`\`Preformatted text\`\`\` to make text preformatted\n"
        r"Use \`\`\`python from time import time\n"
        r"print\(time\(\)\)\`\`\`\n"
        r"Use \>Quote to decorate text as a quote\n"
        r"You can also cobine modifiers but I would rather using aiogram build in helpers for that"
        r"The convenient way to apply modifiers and avoid typos is to use markdown_decoration from aiogram.utils.text_decorations\n"
    )
    msg = (
        # description
        ""
        + f"""
{markdown_decoration.bold("Bold text")}
{markdown_decoration.italic("Italic")}
{markdown_decoration.underline("Underlined")}
{markdown_decoration.strikethrough("strikethrough text")}
{markdown_decoration.spoiler("Spoiler")}
{markdown_decoration.link("Google link", "https://google\.com")}
{markdown_decoration.code("Monowidth text")}
{markdown_decoration.pre("Preformatted text")}
{markdown_decoration.pre_language("if True: print('Success')", "python")}
{markdown_decoration.expandable_blockquote("""This is an expandeble quote\.
Only beginning of the quote is visible\. To see the whole quote user should click on it
Lorem ipsum dolor sit amet consectetur adipisicing elit\. Cumque accusantium quos voluptas corrupti earum reprehenderit porro debitis ut labore quaerat, illum soluta vel praesentium quo commodi veniam\! Vero laborum reiciendis dicta, laudantium voluptatem eius assumenda ut modi atque ipsam neque non voluptatum\! Quisquam modi, neque in porro accusamus quasi autem\?""")}
{markdown_decoration.bold(markdown_decoration.underline("Bold and underlined text"))}"""
    )
    await handle_callback(callback, msg, "MarkdownV2")

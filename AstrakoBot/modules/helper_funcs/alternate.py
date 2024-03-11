from telegram.error import BadRequest
from functools import wraps
from telegram import ChatAction, Update
from telegram.ext import CallbackContext


def send_message(message, text, *args, **kwargs):
    try:
        return message.reply_text(text, *args, **kwargs)
    except BadRequest as err:
        if str(err) == "Cavab mesajı tapılmadı":
            return message.reply_text(text, quote=False, *args, **kwargs)


def typing_action(func):
    """Func əmrini işləyərkən yazma əməliyyatı göndərir."""

    @wraps(func)
    def command_func(update: Update, context: CallbackContext, *args, **kwargs):
        context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action=ChatAction.TYPING
        )
        return func(update, context, *args, **kwargs)

    return command_func

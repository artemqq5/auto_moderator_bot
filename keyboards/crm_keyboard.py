from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from constants.buttons_ import ADD_CHANNEL, SHOW_CHANNELS


def set_crm_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text=ADD_CHANNEL)],
        [KeyboardButton(text=SHOW_CHANNELS)]
    ]
    return ReplyKeyboardMarkup(keyboard=kb)

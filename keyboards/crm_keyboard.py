from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from constants.buttons_ import ADD_CHANNEL, SHOW_CHANNELS
from constants.messages_ import SKIP, CANCEL_, CREATE_LINK_NOW, PREVIEW_HELLO_MESSAGE, NO, YES

kb_crm = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=ADD_CHANNEL)],
    [KeyboardButton(text=SHOW_CHANNELS)]
])

kb_skip = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=SKIP)],
    [KeyboardButton(text=CANCEL_)]
])

kb_create_link = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=CREATE_LINK_NOW)],
    [KeyboardButton(text=PREVIEW_HELLO_MESSAGE)],
    [KeyboardButton(text=CANCEL_)]
])

kb_cencel = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=CANCEL_)]
])

kb_delete_channel = ReplyKeyboardBuilder(markup=[
    [KeyboardButton(text=YES)],
    [KeyboardButton(text=NO)],
    [KeyboardButton(text=CANCEL_)]
])

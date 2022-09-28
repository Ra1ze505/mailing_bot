from telethon import Button
from telethon.client import ButtonMethods

start_markup = ButtonMethods.build_reply_markup(
    [
        [Button.text("Погода", resize=True), Button.text("Курс"), Button.text("Новости")],
        [Button.text("Изменить город"), Button.text("Изменить время рассылки")],
        [Button.text("О боте"), Button.text("Написать нам")],
    ]
)

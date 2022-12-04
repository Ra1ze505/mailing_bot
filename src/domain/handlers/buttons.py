from telethon import Button
from telethon.client import ButtonMethods

start_markup = ButtonMethods.build_reply_markup(
    [
        [
            Button.text("Погода", resize=True),
            Button.text("Курс"),
            Button.text("Новости"),
        ],
        [Button.text("Изменить город"), Button.text("Изменить время рассылки")],
        [Button.text("О боте"), Button.text("Написать нам")],
    ]
)

weather_markup = ButtonMethods.build_reply_markup(
    [Button.inline("Погода на день", data="weather_by_day")]
)

change_city_markup = ButtonMethods.build_reply_markup(
    [
        [Button.text("Москва", resize=True), Button.text("Санкт-Петербург")],
        [Button.text("Отмена")],
    ]
)


change_time_markup = ButtonMethods.build_reply_markup(
    [
        [Button.text("8:00", resize=True), Button.text("10:00"), Button.text("12:00")],
        [Button.text("Отмена")],
    ]
)

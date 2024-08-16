from aiogram import Bot

from constants.messages_ import NOTIFICATION_NEW_USER
from data.repositories.UserRepository import UserRepository


class AddUserNotify:
    @staticmethod
    async def user_activate_bot(user_id, bot, channel):
        counter = 0
        admins = UserRepository().admins()
        user = UserRepository().get_user(user_id)

        for admin in admins:
            try:
                await bot.send_message(
                    chat_id=admin['user_id'],
                    text=NOTIFICATION_NEW_USER.format(user['username'], user['user_id'], channel, user['time_added_at'])
                )
                counter += 1
            except Exception as e:
                print(f"user_activate_bot: {e}")

        print(f"messaging user_activate_bot {counter}/{len(admins)}")


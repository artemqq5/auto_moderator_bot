from data.DefaultDataBase import DefaultDataBase


class UserRepository(DefaultDataBase):

    def __init__(self):
        super().__init__()

    def add_user(self, user_id, username, firstname, lastname, channel_id=None):
        command = "INSERT INTO `users` (`user_id`, `username`, `firstname`, `lastname`, `channel_id`) VALUES (%s, %s, %s, %s, %s);"
        return self._insert(command, (user_id, username, firstname, lastname, channel_id))

    def get_user(self, user_id):
        command = "SELECT * FROM `users` WHERE `user_id` = %s;"
        return self._select_one(command, (user_id,))


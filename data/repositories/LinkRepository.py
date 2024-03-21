from data.DefaultDataBase import DefaultDataBase


class LinkRepository(DefaultDataBase):

    def __init__(self):
        super().__init__()

    def add_link(self, channel_id, channel_title, link_title, hello_message, link, user_id):
        COMMAND_ = "INSERT INTO `links` (`channel_id`, `channel_title`, `link_title`, `hello_message`, `link`, `created_by`) VALUES (%s, %s, %s, %s, %s, %s);"
        return self._insert(COMMAND_, (channel_id, channel_title, link_title, hello_message, link, user_id))

    def get_link(self, link):
        COMMAND_ = "SELECT * FROM `links` WHERE `link` = %s;"
        return self._select_one(COMMAND_, (link,))

    def update_link(self, user_join, link):
        COMMAND_ = "UPDATE `links` SET `users_join` = %s WHERE `link` = %s;"
        return self._select_one(COMMAND_, (user_join, link))

    def get_all(self, channel_id):
        COMMAND_ = "SELECT * FROM `links` WHERE `channel_id` = %s ORDER BY `_at` DESC;"
        return self._select_all(COMMAND_, (channel_id,))

    def delete_link(self, link):
        COMMAND_ = "DELETE FROM `links` WHERE `link` = %s;"
        return self._delete(COMMAND_, (link,))

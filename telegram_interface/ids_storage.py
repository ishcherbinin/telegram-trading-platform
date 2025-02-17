from typing import Union, Optional


class TgIdsStorage:

    """
    Class represents storage for ids, coming from env variables and from TG chats
    IT might be used to reused messages or reply to users
    """


    def __init__(self):
        self._managers_ids: list[str] = []
        self._chat_per_user_ids: dict[str, str] = {}

    def __repr__(self):
        return (f"{self.__class__.__name__}(Managers chat ids: {self._managers_ids}, "
                f"chat user ids: {self._chat_per_user_ids})")

    def set_managers_ids(self, ids: Union[list[str], str]) -> None:
        if isinstance(ids, str):
            self._managers_ids.append(ids)
        else:
            self._managers_ids.extend(ids)

    def add_user_ids(self, username: str, ids: str):
        self._chat_per_user_ids[username] = ids

    def get_managers_ids(self) -> list[str]:
        return self._managers_ids

    def get_user_ids(self, username: str) -> Optional[str]:
        return self._chat_per_user_ids.get(username, None)


    def get_all_users(self) -> list[str]:
        return list(self._chat_per_user_ids.keys())

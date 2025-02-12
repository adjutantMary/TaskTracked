class UserRequestBody:
    def __init__(
        self,
        id: int | None = None,
        username: str | None = None,
        email: str | None = None,
    ):
        self.id = id
        self.username = username
        self.email = email

    def to_dict(self) -> dict:
        data = {"id": self.id, "username": self.username, "email": self.email}

        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class TaskRequestBody:
    def __init__(
        self,
        id: int | None = None,
        user_id: int | None = None,
        title: str | None = None,
        description: str | None = None,
        due_date: str | None = None,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.due_date = due_date

    def to_dict(self) -> dict:
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
        }

        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data

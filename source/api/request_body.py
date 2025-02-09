


class UserRequestBody:
    def __init__(self, id: int | None = None,
                 username: str | None = None,
                 email: str | None = None,
                 tasks: list[dict] | None = None):
        self.id = id
        self.username = username
        self.email = email
        self.tasks = tasks
        

    def to_dict(self) -> dict:
        data = {'id': self.id, 'username': self.username, 'email': self.email, "tasks": self.tasks}
        
        # Создаем копию словаря, чтобы избежать изменения словаря во время итерации
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data
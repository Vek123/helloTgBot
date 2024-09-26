class User:
    def __init__(self, user_id: int, name: str, created_at: str):
        self._id = user_id
        self.name = name
        self.created_at = created_at

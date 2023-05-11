from encryption import encrypt_aes_cbc


class Note:
    def __init__(
        self,
        id: str,
        name: str,
        content: str,
        is_favorite: bool,
        is_deleted: bool = False,
    ):
        self.id = id
        self.name = "" if name is None else name
        self.content = "" if content is None else content
        self.is_favorite = is_favorite
        self.is_deleted = is_deleted

    def encrypt_sensitive_fields(self, encryption_key: bytes) -> None:
        self.name = encrypt_aes_cbc(
            data_to_encrypt=self.name.encode(), encryption_key=encryption_key
        )
        self.content = encrypt_aes_cbc(
            data_to_encrypt=self.content.encode(), encryption_key=encryption_key
        )

    def __repr__(self):
        return (
            f"\n***Note***\n"
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"content: {self.content}\n"
            f"is_favorite: {self.is_favorite}\n"
            f"is_deleted: {self.is_deleted}"
            f"\n***Note***"
        )

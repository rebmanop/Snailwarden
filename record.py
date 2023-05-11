from encryption import encrypt_aes_cbc


class Record:
    def __init__(
        self,
        id: str,
        name: str,
        login: str,
        password: str,
        is_favorite: bool,
        is_deleted: bool = False,
    ):
        self.id = id
        self.name = "" if name is None else name
        self.login = "" if login is None else login
        self.password = "" if password is None else password
        self.is_favorite = is_favorite
        self.is_deleted = is_deleted

    def encrypt_sensitive_fields(self, encryption_key: bytes) -> None:
        self.name = encrypt_aes_cbc(
            data_to_encrypt=self.name.encode(), encryption_key=encryption_key
        )
        self.login = encrypt_aes_cbc(
            data_to_encrypt=self.login.encode(), encryption_key=encryption_key
        )
        self.password = encrypt_aes_cbc(
            data_to_encrypt=self.password.encode(), encryption_key=encryption_key
        )

    def __repr__(self):
        return (
            f"\n***Record***\n"
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"login: {self.login}\n"
            f"password: {self.password}\n"
            f"is_favorite: {self.is_favorite}\n"
            f"is_deleted: {self.is_deleted}\n"
            f"additional_fields: {self.additional_fields}"
            f"\n***Record***"
        )

from encryption import encrypt_aes_cbc


class AdditionalField:
    def __init__(
        self,
        id: str,
        name: str,
        value: str,
        record_id: str,
    ):
        self.id = id
        self.name = "" if name is None else name
        self.value = "" if value is None else value
        self.record_id = record_id

    def encrypt_sensitive_fields(self, encryption_key: bytes) -> None:
        self.name = encrypt_aes_cbc(
            data_to_encrypt=self.name.encode(), encryption_key=encryption_key
        )
        self.value = encrypt_aes_cbc(
            data_to_encrypt=self.value.encode(), encryption_key=encryption_key
        )

    def __repr__(self):
        return (
            f"\n***AdditionalField***\n"
            f"id: {self.id}\n"
            f"name: {self.name}\n"
            f"value: {self.value}"
            f"\n***AdditionalField***"
        )

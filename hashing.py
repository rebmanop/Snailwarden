import base64
import hashlib


def hash_master_password(
    master_password: str, salt: str, number_of_times: int, return_raw: bool = False
) -> str | bytes:
    """Hashes master password with PBKDF2(sha-512) specified number of times"""

    # convert recived password hash and salt to bytes
    master_password = master_password.encode("utf-8")
    salt = salt.encode("utf-8")

    # hash password "number_of_times" with salt
    hashed_master_password = hashlib.pbkdf2_hmac(
        hash_name="sha512",
        password=master_password,
        salt=salt,
        iterations=number_of_times,
        dklen=32,
    )

    if return_raw == True:
        return hashed_master_password

    # convert to base64
    result = base64.b64encode(hashed_master_password)

    # convert to string
    result = result.decode()

    return result

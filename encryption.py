import base64
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util import Padding
from config import DATA_AND_IV_DELIMETER


def encrypt_aes_cbc(data_to_encrypt: bytes, encryption_key: bytes) -> str:
    """Encrypts data using AES-256-CBC with pkcs7 padding and random 16 byte IV.
    Returns <encrypted_data>:<iv> as base64 string"""

    # apply padding to data
    data_to_encrypt = Padding.pad(
        data_to_encrypt, block_size=AES.block_size, style="pkcs7"
    )

    # generate random 16 bytes IV
    iv = Random.new().read(AES.block_size)

    # create a cipher object with necessary parameters
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)

    # encrypt data
    encrypted_data = cipher.encrypt(data_to_encrypt)

    # convert encrypted data and IV to base64
    encrypted_data = base64.b64encode(encrypted_data).decode()
    iv = base64.b64encode(iv).decode()

    return encrypted_data + DATA_AND_IV_DELIMETER + iv

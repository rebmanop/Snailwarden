import requests
from requests import Response
from base64 import b64encode
from config import SNAILPASS_SERVER_URL, NUMBER_OF_HASH_ITERATIONS_FOR_LOGIN
from hashing import hash_master_password
from record import Record
from note import Note
from additional_field import AdditionalField


class API:
    @staticmethod
    def login(email: str, master_password: str) -> Response:
        hashed_master_password = hash_master_password(
            master_password,
            salt=email,
            number_of_times=NUMBER_OF_HASH_ITERATIONS_FOR_LOGIN,
        )
        auth_str = f"{email}:{hashed_master_password}"
        credentials = b64encode(auth_str.encode()).decode("utf-8")
        response = requests.get(
            SNAILPASS_SERVER_URL + "/login",
            headers={"Authorization": f"Basic {credentials}"},
        )

        return response

    @staticmethod
    def post_item(
        item: Record | Note | AdditionalField, session_token: str
    ) -> Response:
        headers = {"x-access-token": f"{session_token}"}

        response: Response = None

        if type(item) == Record:
            response = requests.post(
                SNAILPASS_SERVER_URL + "/records",
                headers=headers,
                json=item.__dict__,
            )
        elif type(item) == Note:
            response = requests.post(
                SNAILPASS_SERVER_URL + "/notes",
                headers=headers,
                json=item.__dict__,
            )
        elif type(item) == AdditionalField:
            response = requests.post(
                SNAILPASS_SERVER_URL + "/additional_fields",
                headers=headers,
                json=item.__dict__,
            )

        return response

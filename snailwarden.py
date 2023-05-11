import time
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
from api import API
from hashing import hash_master_password
from config import NUMBER_OF_HASH_ITERATIONS_FOR_ENCRYPTION_KEY, TITLE
from exceptions import LoadFileException
from bitwarden_parser import BitwardenParser
from rich.progress import track


def main() -> None:
    session_token = None
    console = Console()

    title = Markdown(TITLE, style="bold underline blue")
    console.clear()
    console.print(title)

    console.print("Enter your SnailPass credentials:", style="underline")

    snailpass_email = Prompt.ask(
        prompt="email",
    )
    snailpass_master_password = Prompt.ask(
        prompt="master password",
        password=True,
    )

    encryption_key = hash_master_password(
        snailpass_master_password,
        salt=snailpass_email,
        number_of_times=NUMBER_OF_HASH_ITERATIONS_FOR_ENCRYPTION_KEY,
        return_raw=True,
    )

    response = API.login(
        email=snailpass_email, master_password=snailpass_master_password
    )

    if response.status_code == 200:
        console.print("INFO: Login successfull!", style="green")
        session_token = response.json()["token"]
    else:
        console.print(
            f"ERROR: Login failed: {response.json()['message']['error']}\nExiting the application...",
            style="red",
        )
        time.sleep(2.0)
        console.clear()
        exit()

    console.print(
        "\nEnter path to an unencrypted file exported from Bitwarden (json):",
        style="underline",
    )
    bitwarden_filepath = Prompt.ask("Path")

    try:
        bitwarden_json = BitwardenParser.load_json(bitwarden_filepath)

    except LoadFileException as e:
        console.print(
            "ERROR: " + e.message + "\nExiting the application...",
            style="red",
        )

        time.sleep(2.0)
        console.clear()
        exit()

    items = BitwardenParser.get_items_from_json(bitwarden_json)
    print()
    for item in track(
        items,
        description="Encrypting sensitive fields...",
    ):
        item.encrypt_sensitive_fields(encryption_key)

    warnings: list[str] = []
    for item in track(
        items,
        description="Sending data to the server...",
    ):
        response = API.post_item(item, session_token)

        if response.status_code != 201:
            warnings.append(response.json()["message"]["error"])

    for warning in warnings:
        console.print(
            "WARNING: " + warning,
            style="yellow",
        )

    if len(items) == len(warnings):
        console.print(
            "\nERROR: Done. No items has been imported. Check log for warnings...",
            style="red",
        )
    else:
        console.print(
            f"\nINFO: Done. {len(items) - len(warnings)} out of {len(items)} items has been successfully imported.",
            style="green",
        )


if __name__ == "__main__":
    main()

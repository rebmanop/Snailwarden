import json
from record import Record
from note import Note
from additional_field import AdditionalField
from exceptions import LoadFileException
import rich.progress
from uuid import uuid4


class BitwardenParser:
    @staticmethod
    def load_json(path: str) -> dict:
        try:
            with rich.progress.open(
                path, "rb", description="Loading data from specified file..."
            ) as bitwarden_file:
                bitwarden_json = json.load(bitwarden_file)

            return bitwarden_json
        except Exception:
            raise LoadFileException

    @staticmethod
    def get_items_from_json(
        bitwarden_data: dict,
    ) -> list[Record | Note | AdditionalField]:
        raw_items: dict = bitwarden_data["items"]
        items: list[Record | Note | AdditionalField] = []

        for raw_item in raw_items:
            if raw_item["type"] == 1:
                items.append(
                    Record(
                        id=raw_item["id"],
                        name=raw_item["name"],
                        login=raw_item["login"]["username"],
                        password=raw_item["login"]["password"],
                        is_favorite=raw_item["favorite"],
                    )
                )
                if "fields" in raw_item and len(raw_item["fields"]) != 0:
                    for field in raw_item["fields"]:
                        items.append(
                            AdditionalField(
                                id=str(uuid4()),
                                name=field["name"],
                                value=field["value"],
                                record_id=raw_item["id"],
                            )
                        )
            elif raw_item["type"] == 2:
                items.append(
                    Note(
                        id=raw_item["id"],
                        name=raw_item["name"],
                        content=raw_item["notes"],
                        is_favorite=raw_item["favorite"],
                    )
                )

        return items

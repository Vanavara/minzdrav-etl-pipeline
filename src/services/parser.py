# third party
import ijson
from pathlib import Path


def stream_json_items(json_path: Path):
    with open(json_path, "rb") as file:
        parser = ijson.items(file, "records.item")

        for item in parser:
            yield item

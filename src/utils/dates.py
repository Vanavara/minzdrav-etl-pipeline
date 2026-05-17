# third party
from datetime import datetime, date


def parse_date(value: str | None) -> date | None:
    if not value:
        return None

    return datetime.strptime(value, "%d.%m.%Y").date()

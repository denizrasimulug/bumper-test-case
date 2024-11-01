from ulid import ULID


def random_ulid(hour=None):
    from datetime import datetime, timedelta
    import random

    today = datetime.today()
    random_time = today + timedelta(
        hours=hour or random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
        microseconds=random.randint(0, 999999),
    )
    return str(ULID.from_timestamp(random_time.timestamp()))

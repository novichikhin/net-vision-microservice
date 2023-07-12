import random
import string
import threading
import time
from uuid import UUID

import httpx
import uuid6

SERVER_URL = "http://server:8080"
NUM_ENTRIES_INSERT_MIN = 10
NUM_ENTRIES_INSERT_MAX = 100
RANDOM_TEXT_STR_LEN = 16
OUTPUT_EVERY_TIME_SECS = 10


def add_entry(
        session: httpx.Client,
        uuid: UUID,
        text: str
) -> None:
    response = session.post(f"{SERVER_URL}/new", json={"uuid": str(uuid), "text": text})
    response.raise_for_status()


def delete_received_entries(session: httpx.Client) -> int:
    """
    Функция возвращает кол-во удаленных записей
    """

    response = session.get(f"{SERVER_URL}/?count=10")
    response.raise_for_status()

    entries = response.json()

    num_deleted_records = 0

    for entry in entries:
        uuid = entry["uuid"]
        response = session.delete(f"{SERVER_URL}/{uuid}")
        if not response.is_success:
            continue

        num_deleted_records += 1

    return num_deleted_records


def thread_insert_entries() -> None:
    with httpx.Client() as session:
        while True:
            num_entries_insert = random.randint(NUM_ENTRIES_INSERT_MIN, NUM_ENTRIES_INSERT_MAX)

            for _ in range(num_entries_insert+1):
                random_text = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(RANDOM_TEXT_STR_LEN))

                add_entry(
                    session=session,
                    uuid=uuid6.uuid7(),
                    text=random_text
                )


def main() -> None:
    thread = threading.Thread(target=thread_insert_entries)
    thread.start()

    num_deleted_records = 0
    last_check_time = time.perf_counter()

    with httpx.Client() as session:
        while True:
            num_deleted_records += delete_received_entries(session=session)

            current_perf_counter = time.perf_counter()
            if current_perf_counter - last_check_time >= OUTPUT_EVERY_TIME_SECS:
                print(f"Количество удаленных записей: {num_deleted_records}")
                num_deleted_records = 0
                last_check_time = current_perf_counter


if __name__ == "__main__":
    main()

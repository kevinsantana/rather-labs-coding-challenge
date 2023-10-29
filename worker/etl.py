import os
import sys
import json

from string import ascii_letters
from decimal import Decimal, ROUND_DOWN
from random import choice, choices, randint, uniform

from loguru import logger
from dotenv import load_dotenv
from alive_progress import alive_bar

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from psycopg2.extensions import parse_dsn


def set_up():
    # load project envs
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    load_dotenv(os.path.join(BASE_DIR, "worker", ".env"), override=True)
    sys.path.append(BASE_DIR)

    def serialize(record):
        subset = {
            "timestamp": record["time"].timestamp(),
            "file.name": record["file"].path,
            "func": record["function"],
            "line.number": record["line"],
            "log.level": record["level"].name,
            "message": record["message"],
            "exception": record["exception"],
            **record["extra"],
        }
        return json.dumps(subset, default=str)

    def sink(message):
        serialized = serialize(message.record)
        print(serialized)

    def formatter(record):
        # Note this function returns the string to be formatted, not the actual message to be logged
        # return "{time:YYYY-MM-DD HH:mm:ss} [application_name] [{extra[correlationId]}] [{level}] - {name}:{function}:{line} - {message}\n"
        return "{time} | {level: <8} | {name: ^15} | {function: ^15} | {line: >3} | {message}"

    logger.remove()
    logger.add(sink, format=formatter)
    logger.level("ETL", no=37, color="<blue>")
    logger.level("ETL STATUS", no=36, color="<magenta>")


def connect_db():
    while True:
        try:
            connection = psycopg2.connect(**parse_dsn(os.getenv("DB_URI")))
            if connection:
                cursor = connection.cursor(cursor_factory=DictCursor)
                return cursor, connection
        except OperationalError as op_error:
            logger.bind(**{"error": op_error}).error(
                "Database connection error occurred."
            )


def disconnect_db(cursor, connection):
    cursor.close()
    connection.close()


def insert_product(cursor, conn, product_data: dict) -> int:
    cursor.execute(
        """
        INSERT INTO public.product (name, description, price, quantity, category)
        VALUES (%(name)s, %(description)s, %(price)s, %(quantity)s, %(category)s)
        RETURNING id
        """,
        product_data,
    )
    conn.commit()
    product_id = cursor.fetchone()["id"]
    return product_id if product_id else 0


def create_random_product() -> dict:
    return {
        "name": "".join(choices(ascii_letters, k=randint(1, 255))),
        "description": "".join(choices(ascii_letters, k=randint(1, 255))),
        "price": Decimal(uniform(1, 10_000_000)).quantize(
            Decimal(".10"), rounding=ROUND_DOWN
        ),
        "quantity": randint(1, 10_000),
        "category": choice(["Eletronics", "Clothing", "Food"]),
    }


def etl(n_products: int = 100_000):
    logger.log("ETL STATUS", "[-] ETL NOT READY")
    cur, conn = connect_db()
    with alive_bar(n_products) as bar:
        for i in range(1, n_products + 1):
            try:
                logger.log("ETL", f"INSERTING {i}/{n_products}")
                product = create_random_product()
                product_id = insert_product(cur, conn, product)
                if not product_id:
                    extra = {
                        "error": error,
                        "iteration": f"{i}/{n_products}",
                        "conn": conn,
                        "product": product,
                        "product_id": product_id,
                    }
                    logger.bind(**extra).log("ETL", "insertion error")
                    continue
                bar()
            except Exception as error:
                extra = {
                    "error": error,
                    "iteration": f"{i}/{n_products}",
                    "conn": conn,
                    "product": product if product else None,
                    "product_id": product_id,
                }
                logger.bind(**extra).log("ETL", "exception not handled")
                continue
    logger.log("ETL STATUS", "[+] ETL FINISHED")


if __name__ == "__main__":
    set_up()
    etl()

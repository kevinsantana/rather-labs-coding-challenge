import abc
import functools

import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor
from psycopg2.extensions import parse_dsn

from loguru import logger

from product_inventory.config import envs
from product_inventory.exceptions import ErrorDetails
from product_inventory.exceptions.database import RequiredFieldsException


def fields_obrigatorios(fields):
    """
    For any database operation (DDL or DML) guaruatees that the required fields
    for such operations are passed, otherwise, throws exception.
    :param fields: field(s) necessário(s) para a transação.
    :raises RequiredFieldsException: If any of the required fields are not passed.
    """

    def decorator_required_fields(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            for field in fields:
                if self.dict().get(field) is None:
                    raise RequiredFieldsException(
                        status=403,
                        error="Forbidden",
                        message="required field not passed",
                        error_details=[
                            ErrorDetails(
                                message=f"{self.__class__.__name__}: {field} not passed"
                            ).to_dict()
                        ],
                    )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator_required_fields


class DataBase:
    """
    Each database table is represented as a class, with columns as attributes and
    class methods as transactions (DML or DDL). Database operation results are
    dictionaries with keys corresponding to table columns, using the DictCursor
    cursor factory. Classes inheriting from DataBase must implement the dict method
    to instantiate table objects and map attributes to table columns. This object-oriented
    approach eliminates the need for other classes to implement common database
    table transactions such as insert, find_one, and find_all.

    """

    def __connect(self):
        """
        Establishes a database connection using connection data sourced from
        environment variables exported in the product_inventory/config/envs.py file.
        :raises OperationalError: Could not establish a connection.
        """
        while True:
            try:
                self.__connection = psycopg2.connect(**parse_dsn(envs.DB_URI))
                if self.__connection:
                    self.__cursor = self.__connection.cursor(cursor_factory=DictCursor)
                    break
            except OperationalError as op_error:
                logger.bind(**{"error": op_error}).error(
                    "Database connection error occurred."
                )
                continue

    def __disconect(self):
        """
        Closes the database connection.
        """
        self.__cursor.close()
        self.__connection.close()

    def insert(self):
        """
        Inserts data into the database. Classes inheriting from DataBase should
        be instantiated with the query_string and dict methods to map object values
        in the database transaction.

        .. code-block:: python

            self.__cursor.execute('''
                        INSERT INTO some_table (an_int, a_date, another_date, a_string)
                        VALUES (%(int)s, %(date)s, %(date)s, %(str)s);
                        ''',
                        {'int': 10, 'str': "O'Reilly", 'date': datetime.date(2005, 11, 18)})

        The connection opens and closes promptly, preventing unnecessary open connections.
        :return: The number of affected rows: 1 on success, None on failure.
        :rtype: int or None
        """
        self.__connect()
        self.__cursor.execute(self.query_string, self.dict())
        self.__connection.commit()
        result = self.__cursor.rowcount
        self.__disconect()
        return result

    def find_one(self):
        """
        Retrieves the next database row impacted by the query in query_string.
        If no record exists, it returns None. The connection is promptly opened
        and closed to prevent unnecessary openings.
        :return: Query result.
        :rtype: dict
        """
        self.__connect()
        self.__cursor.execute(self.query_string, self.dict())
        result = self.__cursor.fetchone()
        self.__disconect()
        return result

    def find_all(self, total=False):
        """
        Retrieves all database rows impacted by the query in query_string. Returns
        an empty list if no records exist. The connection opens and closes promptly,
        preventing unnecessary openings.
        :param bool total: Retrieve the total number of search records.
        :return: Query result.
        :rtype: list
        """
        self.__connect()
        self.__cursor.execute(self.query_string, self.dict())
        result = self.__cursor.fetchall()
        self.__disconect()
        if total:
            return result, self.__cursor.rowcount
        return result

    @abc.abstractclassmethod
    def dict(self):
        raise NotImplementedError

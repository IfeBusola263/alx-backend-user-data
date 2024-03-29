#!/usr/bin/env python3
"""
This module implements functions, methods and class that demonstrate
> How to implement a log filter that will obfuscate PII fields
> How to encrypt a password and check the validity of an input password
> How to authenticate to a database using environment variables
"""
from typing import List, Tuple
import re
import logging
import mysql.connector
import os
import csv
import datetime


# file = open('user_data.csv')
# csv_reader = csv.reader(file)
csv_fields = [
    "name", "email", "phone", "ssn", "password",
    "ip", "last_login", "user_agent",
    ]

PII_FIELDS: Tuple[str] = ("name", "email", "ssn", "password", "phone")
# tuple(csv_fields[:-3])


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    This function returns the log message obfuscated.
    >>> filter_datum = __import__('filtered_logger').filter_datum
    >>> fields = ["password", "date_of_birth"]
    >>> messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;
    date_of_birth=12/12/1986;",
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
    >>> for message in messages:
    ...    print(filter_datum(fields, 'xxx', message, ';'))
    ...
    name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
    name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
    >>>
    """
    for field in fields:
        message = re.sub(
            rf'{field}=([^{separator}]+)', f'{field}={redaction}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        '''
        The first method to be called at the instance of the class.
        '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats an instance of a LogRecord with super class format
        """
        record.msg = filter_datum(
            self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    The method returns a 'logging.Logger' object.
    """

    # create logger, set severity and propagation
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # create console handler and add formatter to handler
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

    # add handler to logger
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connection object
    """
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    uname = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')

    connection = mysql.connector.connect(host=host,
                                         database=db,
                                         user=uname,
                                         password=pwd)

    return connection


def main() -> None:
    """
    This function uses the get_db to get a connection and retreive
    the rows in the users table and display each row in a filtered
    format.
    """

    # query database for the information
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    # store information in a list
    info = [list(zip(csv_fields, row)) for row in cursor]

    # get a logger and log the information
    logger = get_logger()

    for line in info:
        msg = ''
        for key_val in line:
            if isinstance(key_val[1], datetime.datetime):
                val = key_val[1].strftime('%Y-%m-%d %H:%M:%S')
            else:
                val = key_val[1]
            msg = msg + key_val[0] + '=' + val + ';'

        logger.info(msg)

    # close all connections
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

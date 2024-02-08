#!/usr/bin/env python3
"""
This module implements functions, methods and class that demonstrate
> How to implement a log filter that will obfuscate PII fields
> How to encrypt a password and check the validity of an input password
> How to authenticate to a database using environment variables
"""
from typing import List
import re


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
        if field in message:
            message = re.sub(
                rf'{field}=([^{separator}]+)', f'{field}={redaction}', message)
    return message
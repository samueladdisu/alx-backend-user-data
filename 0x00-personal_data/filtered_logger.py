#!/usr/bin/env python3
"""
Regex scramble user data
"""
from typing import List
import re


import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ initialize """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format log record"""
        res = filter_datum(self.fields,
                           self.REDACTION, record.msg, self.SEPARATOR)

        print(res)
        record.msg = res
        return super().format(record)


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """ Regex filter and replace some data inside string"""
    data = message.split(separator)
    return ";".join([re.sub("(.*=)(.*)", r"\1" + redaction, d)
                     if d.split("=")[0] in fields else d for d in data])

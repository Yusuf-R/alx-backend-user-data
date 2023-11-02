#!/usr/bin/env python3
"""Personal Data Template"""
import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates sensitive data in a log message."""
    for f in fields:
        message = re.sub("{}=.*?{}".format(f, separator),
                         "{}={}{}".format(f, redaction, separator), message)
    return message

#!/usr/bin/env python3
"""Personal Data Template"""
import re
from typing import List
import logging


def filter_datum(fields, redaction, message, separator):
    """Obfuscates sensitive data in a log message."""
    for f in fields:
        message = re.sub("{}=.*?{}".format(f, separator),
                         "{}={}{}".format(f, redaction, separator), message)
    return message

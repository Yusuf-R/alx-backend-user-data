#!/usr/bin/env python3
"""Personal Data Template"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator) -> str:
    """Obfuscates sensitive data in a log message."""
    for f in fields:
        d = re.sub(r"{}=\S+".format(f), "{}={}".format(f, redaction), message)
    return d + separator

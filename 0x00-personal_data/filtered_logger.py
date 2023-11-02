#!/usr/bin/env python3
"""Personal Data Template"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator) -> str:
    """Obfuscates sensitive data in a log message."""
    d = message
    for f in fields:
        d = re.sub(rf'{f}=[^;]+', f'{f}={redaction}', d)
    return d 

#!/usr/bin/env python3
"""Personal Data Template"""
import re


def filter_datum(fields, redaction, message, separator):
    """Obfuscates sensitive data in a log message."""
    for f in fields:
        d = re.sub(r"{}=\S+".format(f), "{}={}".format(f, redaction), message)
    return d + separator

#!/usr/bin/env python3
"""Personal Data Template"""

import re
import logging

# Write a function called filter_datum that returns the log message obfuscated:
# Arguments:
# fields: a list of strings representing all fields to obfuscate
# redaction: a string representing by what the field will be obfuscated
# message: a string representing the log line
# separator: a string representing by which character is separating all
# fields in the log line (message)
# The function should use a regex to replace occurrences of certain field val.
# filter_datum should be less than 5 lines long and use re.sub to perform
# the substitution with a single regex.


def filter_datum(fields, redaction, message, separator):
    """
    Obfuscates sensitive data in a log message.

    Args:
    - fields (list of str): the names of the sensitive fields to obfuscate.
    - redaction (str): the string to use as a replacement for sensitive data.
    - message (str): the log message to obfuscate.
    - separator (str): the string to append at the end of the obfuscated mesg.

    Returns:
    - str: the obfuscated log message, with sensitive fields
      replaced by the redaction string.
    """
    for field in fields:
        data = re.sub(
            r"{}=\S+".format(field), "{}={}".format(field, redaction), message
        )
    data += separator
    return data

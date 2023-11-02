#!/usr/bin/env python3
"""Personal Data Template"""
import re
from typing import List
import logging
import os
import mysql.connector

# ==========================Task2====================================
# Implement a get_logger function that takes no arguments and
# returns a logging.Logger object.
# The logger should be named "user_data" and only log up to logging.INFO level.
# It should not propagate messages to other loggers.
# It should have a StreamHandler with RedactingFormatter as formatter.
# Create a tuple PII_FIELDS constant at the root of the module containing
# the fields from user_data.csv that are considered PII.
# PII_FIELDS can contain only 5 fields - choose the right list of fields that
# can are considered as “important” PIIs or information that you must hide in
# your logs.
# Use it to parameterize the formatter.
# =====================================================================

# =========================Task3====================================
# Database credentials should NEVER be stored in code or checked into
# version control. One secure option is to store them as environment
# variable on the application server.
# In this task, you will connect to a secure holberton database to read a users
# table. The database is protected by a username and password that are set
# as environment variables on the server named
# PERSONAL_DATA_DB_USERNAME (set the default as “root”),
# PERSONAL_DATA_DB_PASSWORD (set the default as an empty string)
# and PERSONAL_DATA_DB_HOST (set the default as “localhost”).
# The database name is stored in PERSONAL_DATA_DB_NAME.
# Implement a get_db function that returns a connector to the
# database (mysql.connector.connection.MySQLConnection object).
# Use the os module to obtain credentials from the environment
# Use the module mysql-connector-python to connect to the MySQL
# database (pip3 install mysql-connector-python)
# =====================================================================

# ========================Task4====================================
# Implement a main function that takes no arguments and returns nothing.
# The function will obtain a database connection using get_db and retrieve
# all rows in the users table and display each row under a filtered format:
# Filtered fields:
# name
# email
# phone
# ssn
# password
# Only your main function should run when the module is executed.


# Create a tuple PII_FIELDS constant at the root of the module containing
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Obfuscates sensitive data in a log message."""
    for f in fields:
        message = re.sub("{}=.*?{}".format(f, separator),
                         "{}={}{}".format(f, redaction, separator), message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records"""
        return (filter_datum(self.fields, self.REDACTION,
                             super(RedactingFormatter, self).format(record),
                             self.SEPARATOR))


def get_logger() -> logging.Logger:
    """Retur a logging.Logger object"""
    # logger = logging.getLogger('user_data')
    # logger.setLevel(logging.INFO)
    # logger.propagate = False
    # handler = logging.StreamHandler()
    # handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # logger.addHandler(handler)
    # return logger
    # OR :
    logger = logging.Logger(name="user_data")
    logger.setLevel = logging.INFO
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    A function that returns a connector to the database
    Args:
        None
    Returns:
        mysql.connector.connection.MySQLConnection:
            A connector to the database
    """
    try:
        # Obtain database credentials from environment variables
        db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
        db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', 'Remisql@91')
        db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
        db_name = os.getenv('PERSONAL_DATA_DB_NAME', 'my_db')
        # Establish connection to the database
        conn = mysql.connector.connection.MySQLConnection(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        return conn
    except mysql.connector.ConnectionError:
        return None


def main():
    """Main function"""
    # establish db connection
    db = get_db()
    cursor = db.cursor()
    # create our logging object
    logger = get_logger()
    # query db
    db_fields = "name, email, phone, ssn, password, ip, last_login, user_agent"
    query = "SELECT {} FROM users".format(db_fields)
    cursor.execute(query)
    data = cursor.fetchall()
    # create the fmt variable needed for our logging.Formatter class
    fmt = "name={}; email={}; phone={}; ssn={}; password={};" + \
          "ip={}; last_login={}; user_agent={}"
    # fill the fmt variable with the data from the db
    for row in data:
        fmt = fmt.format(row[0], row[1], row[2], row[3], row[4], row[5],
                         row[6], row[7])
        # log the data
        logger.info(fmt)
    # close cursor
    cursor.close()
    # close
    db.close()


if __name__ == "__main__":
    main()

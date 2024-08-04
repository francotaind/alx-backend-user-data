#!/usr/bin/env python3
"""
Script for handling Personal Data
"""

import os
import re
import logging
import mysql.connector
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ format record """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated """
    pattern = r"(\w+)=([a-zA-Z0-9@\.\-\(\)\ \:\^\<\>\~\$\%\@\?\!\/]*)"
    return re.sub(pattern,
                  lambda match: match.group(1) + "=" + redaction
                  if match.group(1) in fields else match.group(0), message)


def get_logger() -> logging.Logger:
    """ return a logger object """
    lg = logging.getLogger("user_data")
    lg.setLevel(logging.INFO)
    lg.propagate = False
    sh = logging.StreamHandler()
    sh.setFormatter(RedactingFormatter(PII_FIELDS))
    lg.addHandler(sh)
    return lg


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Creates a connector to a database.
    """
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main():
    """ main function """
    con = get_db()
    cursor = con.cursor()
    query = """
    SELECT name, email, phone, ssn, password, ip, last_login, user_agent
    FROM users;
    """
    cursor.execute(query)
    logger = get_logger()

    for (
        name, email, phone, ssn, password, ip, last_login, user_agent
    ) in cursor:
        message = (
            f"name={name}; email={email}; phone={phone}; ssn={ssn}; "
            f"password={password}; ip={ip}; last_login={last_login}; "
            f"user_agent={user_agent};"
        )
        logger.info(message)

    cursor.close()
    con.close()


if __name__ == "__main__":
    main()

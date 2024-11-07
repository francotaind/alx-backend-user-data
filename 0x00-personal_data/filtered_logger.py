#!/usr/bin/env python3
"""Filtered Logger module."""
import os
import mysql.connector
import logging
from mysql.connector import connection
from typing import List

# Define sensitive fields to redact
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields, redaction, message, separator):
    """Replaces field values with redaction in the log message."""
    for field in fields:
        message = re.sub(f'{field}=[^;]+', f'{field}={redaction}', message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields if fields else []

    def format(self, record: logging.LogRecord) -> str:
        # Filter sensitive fields using filter_datum
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)
        return super().format(record)

def get_logger() -> logging.Logger:
    """Creates and configures a logger named 'user_data' with specific settings."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    # Set up StreamHandler with RedactingFormatter
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.addHandler(stream_handler)
    
    return logger

def get_db() -> connection.MySQLConnection:
    """Creates and returns a secure connection to the database."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    
    db_connection = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )
    return db_connection

def main():
    """Fetch and log user data from the database with PII fields redacted."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    logger = get_logger()

    # Retrieve all data from users table
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    # Log each row after redacting sensitive information
    for row in rows:
        log_message = "; ".join([f"{key}={value}" for key, value in row.items()])
        logger.info(log_message)

    # Clean up
    cursor.close()
    db.close()

# Only run main() when the module is executed directly
if __name__ == "__main__":
    main()


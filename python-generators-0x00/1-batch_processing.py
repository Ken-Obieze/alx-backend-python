#!/usr/bin/python3
"""
Batch processing of users from user_data table in ALX_prodev
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that yields rows in batches of size batch_size
    """
    with mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    ) as connection:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM user_data;")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch

def batch_processing(batch_size):
    """
    Processes each batch and prints users over age 25
    """
    for batch in stream_users_in_batches(batch_size):          # loop 1
        for user in batch:                                     # loop 2
            if user["age"] > 25:
                print(user)

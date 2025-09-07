#!/usr/bin/python3
"""
Batch processing of users from user_data table in ALX_prodev
"""

import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator that yields rows in batches of size batch_size
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",   # change if needed
            password="",   # change if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch and prints users over age 25
    """
    for batch in stream_users_in_batches(batch_size):          # loop 1
        for user in batch:                                     # loop 2
            if user["age"] > 25:
                print(user)

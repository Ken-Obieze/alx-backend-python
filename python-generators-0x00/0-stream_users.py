#!/usr/bin/python3
"""
Generator that streams rows from user_data table in ALX_prodev database
"""

import mysql.connector


def stream_users():
    """Generator that yields rows from user_data one by one"""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root", 
            password="",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row

    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

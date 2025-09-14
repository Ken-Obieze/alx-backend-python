#!/usr/bin/python3
"""
Decorator to log SQL queries
"""

import sqlite3
import functools


def log_queries(func):
    """
    Decorator that logs the SQL query before executing it
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Example: fetch users while logging the query
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    for user in users:
        print(user)
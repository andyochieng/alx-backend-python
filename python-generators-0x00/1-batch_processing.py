#!/usr/bin/env python3
"""Batch processing of users from a database using generators"""

import sqlite3

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the database.
    Each batch is a list of dictionaries of user data.
    """
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # ✅ First loop
        batch.append(dict(row))
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:  # Yield remaining records if any
        yield batch

    conn.close()


def batch_processing(batch_size):
    """
    Processes each batch by filtering users over the age of 25,
    and prints the result one by one.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Second loop
        for user in batch:  # ✅ Third loop
            if user.get("age", 0) > 25:
                print(user)

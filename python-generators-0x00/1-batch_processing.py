#!/usr/bin/env python3
"""Batch processing of user data using generator"""

import sqlite3

def stream_users_in_batches(batch_size):
    """
    Generator that yields user data in batches from the user_data table.
    Each batch is a list of user dictionaries.
    """
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # ✅ Loop 1
        batch.append(dict(row))
        if len(batch) == batch_size:
            yield batch  # ✅ Generator
            batch = []

    if batch:
        yield batch

    conn.close()

def batch_processing(batch_size):
    """
    Processes each batch by filtering users over age 25 and printing them.
    """
    for batch in stream_users_in_batches(batch_size):  # ✅ Loop 2
        for user in batch:  # ✅ Loop 3
            if user.get("age", 0) > 25:
                print(user)

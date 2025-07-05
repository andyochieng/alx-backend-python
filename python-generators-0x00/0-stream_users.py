#!/usr/bin/env python3
"""Generator that streams rows one by one from the user_data table"""

import sqlite3

def stream_users():
    """Yields rows from the user_data table one by one as dictionaries"""
    conn = sqlite3.connect("user_data.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:  # ✅ Only one loop, as required
        yield dict(row)

    conn.close()

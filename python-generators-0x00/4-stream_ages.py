#!/usr/bin/env python3
"""Memory-efficient aggregation using generators"""

import sqlite3

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table
    """
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # ✅ Loop 1
        yield row[0]  # yield the age

    conn.close()


# Calculate average without loading full dataset
total = 0
count = 0

for age in stream_user_ages():  # ✅ Loop 2
    total += age
    count += 1

if count > 0:
    average = total / count
    print(f"Average age of users: {average}")
else:
    print("No users found.")

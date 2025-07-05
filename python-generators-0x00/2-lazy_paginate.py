#!/usr/bin/env python3
"""Lazy loading paginated data from the users database"""

seed = __import__('seed')

def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database
    using LIMIT and OFFSET
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Generator that lazily loads user data in pages of `page_size`
    using only one loop.
    """
    offset = 0
    while True:  # ✅ Single loop only
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page  # ✅ Generator used to lazily return each page
        offset += page_size

"""Handles basic database ops."""

import sqlite3

from models import BlogPost


def create_table():
    """Create the blog post table."""
    connection = sqlite3.connect("posts.db")
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
    )
    connection.commit()
    print(connection.total_changes)
    connection.close()


def insert_post(title: str, content: str):
    """Insert a blog post."""
    connection = sqlite3.connect("posts.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
    connection.commit()
    print(connection.total_changes)
    connection.close()


def get_post(post_id: int) -> BlogPost:
    """Retrieve a blog post by ID."""
    conn = sqlite3.connect("posts.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = cur.fetchone()
    conn.close()

    return BlogPost(id=post[0], title=post[1], content=post[2])


def get_post_list() -> list[dict[str, int | str]]:
    """Retrieve all post IDs and titles from the database."""
    conn = sqlite3.connect("posts.db")
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM posts")
    posts = cur.fetchall()
    conn.close()

    return [dict(id=int(post[0]), title=str(post[1])) for post in posts]


def vulnerable_get_post_by_title(title: str) -> BlogPost:
    """Retrieve a post by title—but it's vulnerable!"""
    conn = sqlite3.connect("posts.db")
    cur = conn.cursor()
    query = f"SELECT * FROM posts WHERE UPPER(title)='{title.upper()}'"
    print(query)
    cur.execute(query)
    post = cur.fetchone()
    conn.close()

    return BlogPost(id=post[0], title=post[1], content=post[2])

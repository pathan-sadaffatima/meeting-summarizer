import sqlite3


DATABASE = "meetings.db"


def get_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS meetings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT NOT NULL,

            transcript TEXT NOT NULL,

            user_prompt TEXT NOT NULL,

            result TEXT NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()


def save_meeting(
    filename,
    transcript,
    user_prompt,
    result
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO meetings (

            filename,
            transcript,
            user_prompt,
            result

        )

        VALUES (?, ?, ?, ?)
        """,
        (
            filename,
            transcript,
            user_prompt,
            result
        )
    )

    connection.commit()

    meeting_id = cursor.lastrowid

    connection.close()

    return meeting_id


def get_meeting(meeting_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM meetings

        WHERE id = ?
        """,
        (meeting_id,)
    )

    meeting = cursor.fetchone()

    connection.close()

    return meeting


def get_all_meetings():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            filename,
            user_prompt,
            created_at

        FROM meetings

        ORDER BY id DESC
        """
    )

    meetings = cursor.fetchall()

    connection.close()

    return meetings
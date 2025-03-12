import sqlite3

DATABASE = 'markers.db'


def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS markers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        latitude REAL,
                        longitude REAL,
                        user_id INTEGER,
                        delete_requests INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()


def add_marker_to_db(latitude, longitude, user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO markers (latitude, longitude, user_id) VALUES (?, ?, ?)",
                   (latitude, longitude, user_id))
    conn.commit()
    conn.close()


def check_marker_exists(latitude, longitude):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM markers WHERE ABS(latitude - ?) < 0.001 AND ABS(longitude - ?) < 0.001",
                   (latitude, longitude))
    existing_marker = cursor.fetchone()
    conn.close()
    return existing_marker is not None


def get_all_markers(marker_id=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    if marker_id:
        cursor.execute("SELECT * FROM markers WHERE id = ?", (marker_id,))
    else:
        cursor.execute("SELECT * FROM markers")
    markers = cursor.fetchall()
    conn.close()
    return markers


def increment_delete_requests(marker_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE markers SET delete_requests = delete_requests + 1 WHERE id = ?", (marker_id,))
    conn.commit()
    conn.close()


def delete_marker_from_db(marker_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM markers WHERE id = ?", (marker_id,))
    conn.commit()
    conn.close()


# Initialize the database
init_db()

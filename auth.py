import hashlib
from database import conn, cursor


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(name, email, password):

    password = hash_password(password)

    try:

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()

        return True

    except:

        return False


def login(email, password):

    password = hash_password(password)

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    return cursor.fetchone()
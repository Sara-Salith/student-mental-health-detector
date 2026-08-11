import streamlit as st
import pandas as pd
import hashlib
import os

USER_FILE = "users.csv"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        return pd.DataFrame(columns=["username", "password"])


def save_user(username, password):
    users = load_users()

    new_user = pd.DataFrame({
        "username": [username],
        "password": [hash_password(password)]
    })

    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USER_FILE, index=False)


def login_user(username, password):

    users = load_users()

    if username.strip() == "" or password.strip() == "":
        return False

    hashed_password = hash_password(password)

    return (
        (users["username"] == username) &
        (users["password"] == hashed_password)
    ).any()


def register_user(username, password, confirm_password):

    if username.strip() == "" or password.strip() == "":
        return False, "Please fill all fields."

    if password != confirm_password:
        return False, "Passwords do not match."

    users = load_users()

    if username in users["username"].values:
        return False, "Username already exists."

    save_user(username, password)

    return True, "Registration successful!"
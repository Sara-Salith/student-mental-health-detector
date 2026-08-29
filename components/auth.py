import streamlit as st
import hashlib
from supabase import create_client


# ----------------------------------------
# SUPABASE CONNECTION
# ----------------------------------------

@st.cache_resource
def get_supabase():

    supabase_url = st.secrets["supabase"]["url"]
    supabase_key = st.secrets["supabase"]["key"]

    return create_client(
        supabase_url,
        supabase_key
    )


# ----------------------------------------
# PASSWORD HASHING
# ----------------------------------------

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ----------------------------------------
# REGISTER USER
# ----------------------------------------

def register_user(
    username,
    password,
    confirm_password
):

    # Check empty fields
    if username.strip() == "" or password.strip() == "":
        return False, "Please fill all fields."

    # Remove accidental spaces
    username = username.strip()

    # Check password confirmation
    if password != confirm_password:
        return False, "Passwords do not match."

    try:

        supabase = get_supabase()

        # Check if username already exists
        existing_user = (
            supabase
            .table("users")
            .select("username")
            .eq("username", username)
            .execute()
        )

        if existing_user.data:
            return False, "Username already exists."

        # Insert new user
        supabase.table("users").insert({
            "username": username,
            "password": hash_password(password)
        }).execute()

        return True, "Registration successful! You can now log in."

    except Exception as e:

        return False, f"Registration failed: {str(e)}"


# ----------------------------------------
# LOGIN USER
# ----------------------------------------

def login_user(
    username,
    password
):

    # Check empty fields
    if username.strip() == "" or password.strip() == "":
        return False

    username = username.strip()

    try:

        supabase = get_supabase()

        # Find user with username
        response = (
            supabase
            .table("users")
            .select("*")
            .eq("username", username)
            .execute()
        )

        # User does not exist
        if not response.data:
            return False

        user = response.data[0]

        # Compare password hashes
        hashed_password = hash_password(password)

        if user["password"] == hashed_password:
            return True

        return False

    except Exception:

        return False
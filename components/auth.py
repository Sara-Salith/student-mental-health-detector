import streamlit as st
import hashlib
from supabase import create_client
import re

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
# PASSWORD VALIDATION
# ----------------------------------------

def validate_password(password):

    # Minimum length
    if len(password) < 6:
        return False, "Password must contain at least 6 characters."

    # Uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least 1 uppercase letter."

    # Lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least 1 lowercase letter."

    # Special character
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least 1 special character."
    
    # Number
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least 1 number."

    return True, "Password is valid."


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

    # Validate password strength
    password_valid, password_message = validate_password(password)

    if not password_valid:
        return False, password_message

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
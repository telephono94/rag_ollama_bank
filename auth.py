import streamlit as st
import json
import os
import hashlib

USERS_FILE = "users.json"

# Passwort hashen
def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Nutzer laden
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

# Nutzer speichern
def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# Registrierung
def register(username, password):
    users = load_users()
    if username in users:
        return False, "Benutzer existiert bereits!"
    users[username] = hash_pw(password)
    save_users(users)
    return True, "Registrierung erfolgreich!"

# Login
def login(username, password):
    users = load_users()
    if username in users and users[username] == hash_pw(password):
        return True
    return False

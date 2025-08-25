import streamlit as st
import sqlite3
import tempfile
import os

@st.cache_resource
def init_database():
    """Initialize database - works on Streamlit Cloud"""
    # Use a temporary file for SQLite on Streamlit Cloud
    db_path = os.path.join(tempfile.gettempdir(), "digital_gold.db")
    
    conn = sqlite3.connect(db_path, check_same_thread=False)
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gold_purchases (
            purchase_id TEXT PRIMARY KEY,
            user_id INTEGER,
            amount DECIMAL(10,2),
            gold_grams DECIMAL(15,6),
            gold_price_per_gram DECIMAL(10,2),
            status TEXT DEFAULT 'SUCCESS',
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    return conn

# Alternative: Use Streamlit's session state for temporary storage
def init_session_storage():
    """Initialize session-based storage"""
    if 'purchases' not in st.session_state:
        st.session_state.purchases = []
    if 'users' not in st.session_state:
        st.session_state.users = {}

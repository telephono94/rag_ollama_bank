import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd

# DB-Pfad
DB_PATH = Path("chat_history.db")

# Verbindung aufbauen
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

st.title("🔍 SQLite DB Checker")

# Alle Tabellen in der DB abfragen
cur.execute("""
SELECT name FROM sqlite_master
WHERE type='table'
ORDER BY name;
""")
tables = cur.fetchall()

if tables:
    st.write(f"**Insgesamt {len(tables)} Tabelle(n) gefunden:**")
    for (table_name,) in tables:
        st.subheader(f"📂 Tabelle: {table_name}")

        # Schema der Tabelle
        cur.execute(f"PRAGMA table_info({table_name});")
        columns = cur.fetchall()
        st.write("**Spalten:**")
        for col in columns:
            col_id, col_name, col_type, notnull, default_value, pk = col
            st.write(f"- {col_name} ({col_type}), NOT NULL={bool(notnull)}, PK={bool(pk)}, Default={default_value}")

        # Anzahl der Einträge
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cur.fetchone()[0]
        st.write(f"**Anzahl der Einträge:** {count}")

        # Für chat_messages: Nachrichten anzeigen, nach Timestamp sortiert
        if table_name == "chat_messages" and count > 0:
            st.write("**Nachrichten (nach Timestamp sortiert):**")

            # Lade alle Nachrichten
            cur.execute("""
                SELECT user, role, content, timestamp
                FROM chat_messages
                ORDER BY timestamp ASC
            """)
            rows = cur.fetchall()

            # In DataFrame umwandeln
            df = pd.DataFrame(rows, columns=["User", "Role", "Content", "Timestamp"])

            # Als interaktive Tabelle anzeigen
            st.dataframe(df, use_container_width=True)

        st.write("---")
else:
    st.write("❌ Keine Tabellen gefunden.")

conn.close()





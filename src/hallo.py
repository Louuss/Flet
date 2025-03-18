import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect("Bank.db")
cursor = conn.cursor()

# Tabelle erstellen
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS benutzer (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         age INTEGER
#     )
# """)

# # Daten einfügen
# cursor.execute("INSERT INTO benutzer (name, age) VALUES (?, ?)", ('Alice', 30))
# cursor.execute("INSERT INTO benutzer (name, age) VALUES (?, ?)", ('Bob', 25))

# # Änderungen speichern
# conn.commit()

# Daten abfragen
cursor.execute("SELECT * FROM benutzer")
db_inhalt = cursor.fetchall()
for row in db_inhalt:
    print(row)
import flet as ft
import mysql.connector

# Verbindung zur Datenbank herstellen
conn = mysql.connector.connect(host="localhost", user="root", password="", database="python_db")
cursor = conn.cursor()

if conn.is_connected():
    print("connected successfully")
else:
    print("failed to connect")

# Tabelle erstellen
cursor.execute("""
    CREATE TABLE if not exists benutzer(
        id INTEGER PRIMARY KEY auto_increment,
        vname VARCHAR(255) NOT NULL,
        nname VARCHAR(255) NOT NULL,
        gebi VARCHAR(255) NOT NULL
    )
""")

def main(page: ft.Page):
    # Save Button
    def save_data(e):
        try:
            if dd.value:  # Wenn ein Eintrag ausgewählt ist, aktualisiere ihn
                cursor.execute("""
                    UPDATE benutzer 
                    SET vname = %s, 
                    nname = %s, 
                    gebi = %s 
                    WHERE id = %s
                """, (vorname_field.value, nachname_field.value, geburtsdatum_field.value, dd.value))
            else:  # Andernfalls füge einen neuen Eintrag hinzu
                cursor.execute("""
                    INSERT INTO benutzer (vname, nname, gebi) 
                    VALUES (%s, %s, %s)
                """, (vorname_field.value, nachname_field.value, geburtsdatum_field.value))
            conn.commit()
            refresh()
            page.update()
            print(f"Gespeichert oder aktualisiert: {dd.value}")
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    # Delete Button
    def del_data(e):
        if dd.value:
            try:
                cursor.execute("DELETE FROM benutzer WHERE id = %s", (dd.value,))
                conn.commit()
                new_data(e)  # Clear the form
                refresh()
            except Exception as e:
                print(f"Fehler beim Löschen: {e}")

    # New Button
    def new_data(e):
        vorname_field.value = ""
        nachname_field.value = ""
        geburtsdatum_field.value = ""
        dd.value = None  # Dropdown zurücksetzen
        page.update()

    # Get DropDown Options
    def get_options():
        options = []
        cursor.execute("SELECT * FROM benutzer")
        db_inhalt = cursor.fetchall()
        for row in db_inhalt:  
            options.append(ft.dropdown.Option(key=row[0], text=f"{row[1]} {row[2]}"))
        return options

    # Refresh DropDown
    def refresh():
        dd.options = get_options()
        # Set the value to the last inserted ID if adding new, or keep current if updating
        if not dd.value and cursor.lastrowid:
            dd.value = cursor.lastrowid
        page.update()
        # Update the form with the current selection
        if dd.value:
            dropdown_changed(None)

    # Dropdown Changed Event
    def dropdown_changed(e):
        selected_id = dd.value
        if selected_id:
            cursor.execute("SELECT * FROM benutzer WHERE id = %s", (selected_id,))
            selected_entry = cursor.fetchone()
            if selected_entry:
                vorname_field.value = selected_entry[1]
                nachname_field.value = selected_entry[2]
                geburtsdatum_field.value = selected_entry[3]
                page.update()

    # Defining DropDown
    dd = ft.Dropdown(
        border=ft.InputBorder.UNDERLINE,
        visible=True,
        options=get_options(),
        on_change=dropdown_changed,
        width=300
    )

    # Defining Texts and Textfields
    vn = ft.Text("Vorname:       ", size=30, color="white")
    nn = ft.Text("Nachname:     ", size=30, color="white")
    gd = ft.Text("Geburtsdatum:", size=30, color="white")
    vorname_field = ft.TextField(label="Vorname", value="", width=300)
    nachname_field = ft.TextField(label="Nachname", value="", width=300)
    geburtsdatum_field = ft.TextField(label="Geburtsdatum", value="", width=300)

    # Defining Buttons and Their Position
    button_row = ft.Row(
        [
            ft.OutlinedButton("Speichern", on_click=save_data),
            ft.OutlinedButton("Löschen", on_click=del_data),
            ft.OutlinedButton("Neu", on_click=new_data),
            dd, 
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=10
    )

    # Rows for Text and Textfields
    text_row = ft.Row([vn, vorname_field], alignment=ft.MainAxisAlignment.START, spacing=20)
    text_row1 = ft.Row([nn, nachname_field], alignment=ft.MainAxisAlignment.START, spacing=20)
    text_row2 = ft.Row([gd, geburtsdatum_field], alignment=ft.MainAxisAlignment.START, spacing=20)
    text_column = ft.Column([text_row, text_row1, text_row2], spacing=20)

    # Page Theme
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)
    page.theme_mode = ft.ThemeMode.DARK
    
    # Page layout
    page.add(
        ft.Container(
            content=text_column,
            padding=20,
            expand=True,
        ),
        ft.Container(
            content=button_row,
            padding=20,
            alignment=ft.alignment.center,
        ),
    )

    # Initial refresh to populate dropdown
    refresh()

try:
    ft.app(main)
finally:
    cursor.close()
    conn.close()
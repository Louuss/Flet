import flet as ft
import sqlite3

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect("Bank.db", check_same_thread=False)
cursor = conn.cursor()

# Tabelle erstellen
cursor.execute("""
    CREATE TABLE IF NOT EXISTS benutzer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vname TEXT NOT NULL,
        nname TEXT NOT NULL,
        gebi TEXT NOT NULL
    )
""")

def main(page: ft.Page):
    # Save Button
    def save_data(e):
        if dd.value:  # Wenn ein Eintrag ausgewählt ist, aktualisiere ihn
            cursor.execute("UPDATE benutzer SET vname = ?, nname = ?, gebi = ? WHERE id = ?", 
                        (vorname_field.value, nachname_field.value, geburtsdatum_field.value, int(dd.value)))
        else:  # Andernfalls füge einen neuen Eintrag hinzu
            cursor.execute("INSERT INTO benutzer (vname, nname, gebi) VALUES (?, ?, ?)", 
                        (vorname_field.value, nachname_field.value, geburtsdatum_field.value))
        conn.commit()
        refresh()
        page.update()
        print(f"Gespeichert oder aktualisiert: {dd.value}")

    # Delete Button
    def del_data(e):
        if dd.value:
            cursor.execute("DELETE FROM benutzer WHERE id = ?", (int(dd.value),))
            conn.commit()
            page.update()
            refresh()

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
            options.append(ft.dropdown.Option(key=int(row[0]), text=str(row[1])+" "+str(row[2])))
        return options

    # Refresh DropDown
    def refresh():
        dd.options = get_options()
        dd.value = cursor.lastrowid
        button_row.controls[-1] = dd
        page.update()

    # Dropdown Changed Event
    def dropdown_changed(e):
        selected_id = dd.value
        if selected_id:
            cursor.execute("SELECT * FROM benutzer WHERE id = ?", (selected_id,))
            selected_entry = cursor.fetchone()
            if selected_entry:
                # Update the input fields with the selected entry's data
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
    )

    # Defining Texts and Textfields
    vn = ft.Text("Vorname", size=30, color="white")
    nn = ft.Text("Nachname:", size=30, color="white")
    gd = ft.Text("Geburtsdatum:", size=30, color="white")
    vorname_field = ft.TextField(label="Vorname", value="")
    nachname_field = ft.TextField(label="Nachname", value="")
    geburtsdatum_field = ft.TextField(label="Geburtsdatum", value="")

    # Defining Buttons and Their Position
    button_row = ft.Row(
        [
            ft.OutlinedButton("Speichern", on_click=save_data),
            ft.OutlinedButton("Löschen", on_click=del_data),
            ft.OutlinedButton("Neu", on_click=new_data),
            dd,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Rows for Text and Textfields
    text_row = ft.Row([vn, vorname_field], alignment=ft.MainAxisAlignment.SPACE_AROUND)
    text_row1 = ft.Row([nn, nachname_field], alignment=ft.MainAxisAlignment.SPACE_AROUND)
    text_row2 = ft.Row([gd, geburtsdatum_field], alignment=ft.MainAxisAlignment.SPACE_AROUND)

    # Page Theme
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.INDIGO)

    # Placing the Rows into Columns
    page.add(
        ft.SafeArea(
            ft.Column(
                [
                    ft.Container(
                        content=text_row,
                        padding=ft.padding.only(left=20, top=20, bottom=20),
                        theme_mode=ft.ThemeMode.DARK,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        expand=True,
                    ),
                    ft.Container(
                        content=text_row1,
                        padding=ft.padding.only(left=20, top=20, bottom=20),
                        theme_mode=ft.ThemeMode.DARK,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        expand=True,
                    ),
                    ft.Container(
                        content=text_row2,
                        padding=ft.padding.only(left=20, top=20, bottom=20),
                        theme_mode=ft.ThemeMode.DARK,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        expand=True,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START
            ),
        ),
        ft.Container(
            content=button_row,
            alignment=ft.alignment.bottom_left,
            padding=ft.padding.only(bottom=20),
        ),
    )

    # Initial refresh to populate dropdown
    refresh()

ft.app(main)
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import sqlite3
import os

selected_database = None  # Variable to store the selected or created database name
db_connection = None  # SQLite database connection


def create_or_choose_a_database(frame_index, frame_label):
    global selected_database, db_connection

    selected_option = dropdown_menus[frame_index].get()

    if selected_option:
        selected_database = selected_option
        connect_to_existing_database(selected_database)
        frame_label.config(text=f"Connected to Database: {selected_database}")


def connect_to_existing_database(database_name):
    global db_connection

    # Connect to an existing SQLite database
    db_connection = sqlite3.connect(f"{database_name}.db")
    # Enable foreign key support
    db_connection.execute("PRAGMA foreign_keys = ON")


def create_new_database():
    new_database_name = simpledialog.askstring(
        "New Database", "Enter a name for the new database:")
    if new_database_name:
        create_new_database_in_frame0(new_database_name)
        refresh_dropdowns()
        frame0_label.config(text=f"Database {new_database_name} created")


def create_new_database_in_frame0(database_name):
    global db_connection

    # Create a new SQLite database
    db_connection = sqlite3.connect(f"{database_name}.db")
    # Enable foreign key support
    db_connection.execute("PRAGMA foreign_keys = ON")
    db_connection.commit()


def refresh_dropdowns():
    databases_folder = os.path.dirname(os.path.abspath(__file__))
    databases = [f.replace(".db", "") for f in os.listdir(
        databases_folder) if f.endswith('.db')]
    for dropdown_menu, frame_label in zip(dropdown_menus[1:], frame_labels[1:]):
        current_value = dropdown_menu.get()
        dropdown_menu['values'] = databases
        if current_value in databases:
            dropdown_menu.set(current_value)
        else:
            dropdown_menu.set("Select Database")
            if frame_label:
                frame_label.config(text=f"Database {current_value} deleted")
                selected_database = None


def delete_database():
    selected_option = dropdown_menu3.get()
    if selected_option:
        confirmation = messagebox.askyesno(
            "Delete Database", f"Are you sure you want to delete {selected_option} database?")
        if confirmation:
            delete_database_file(selected_option)
            refresh_dropdowns()


def delete_database_file(database_name):
    # Delete the database file
    database_file = f"{database_name}.db"
    if os.path.exists(database_file):
        os.remove(database_file)


# Window
window = tk.Tk()
window.title('Window of widgets')
window.geometry('800x500+900+100')
window.attributes('-alpha', 0.8)

# Frame 0
frame0 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame0.grid(row=0, column=0, sticky='nsew', padx=20, pady=5)

# Create a style for ttk frames
style = ttk.Style()
style.configure("My.TFrame", background="grey")

create_button = ttk.Button(
    frame0, text='Create Database', command=create_new_database)
create_button.pack(pady=10)
frame0_label = ttk.Label(frame0, text='', background='green')
frame0_label.pack()

# Frame 1
frame1 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame1.grid(row=1, column=0, sticky='nsew', padx=20, pady=5)

databases_folder = os.path.dirname(os.path.abspath(__file__))
databases = [f.replace(".db", "")
             for f in os.listdir(databases_folder) if f.endswith('.db')]

frame1_selection = tk.StringVar()
dropdown_menu1 = ttk.Combobox(
    frame1, values=databases, state='readonly', textvariable=frame1_selection)
dropdown_menu1.set("Select Database")
dropdown_menu1.pack(padx=20, pady=5)

button_perform_action1 = ttk.Button(
    frame1, text='Choose Database', command=lambda: create_or_choose_a_database(1, frame1_label))
button_perform_action1.pack()
frame1_label = ttk.Label(frame1, text='', background='green')
frame1_label.pack()

# Frame 2
frame2 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame2.grid(row=2, column=0, sticky='nsew', padx=20, pady=5)

frame2_selection = tk.StringVar()
dropdown_menu2 = ttk.Combobox(
    frame2, values=databases, state='readonly', textvariable=frame2_selection)
dropdown_menu2.set("Select Database")
dropdown_menu2.pack(padx=20, pady=5)

button_perform_action2 = ttk.Button(
    frame2, text='Choose Database', command=lambda: create_or_choose_a_database(2, frame2_label))
button_perform_action2.pack()
frame2_label = ttk.Label(frame2, text='', background='green')
frame2_label.pack()

# Frame 3
frame3 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame3.grid(row=3, column=0, sticky='nsew', padx=20, pady=5)

frame3_selection = tk.StringVar()
dropdown_menu3 = ttk.Combobox(
    frame3, values=databases, state='readonly', textvariable=frame3_selection)
dropdown_menu3.set("Select Database")
dropdown_menu3.pack(padx=20, pady=5)

button_perform_action3 = ttk.Button(
    frame3, text='Choose Database', command=lambda: create_or_choose_a_database(3, frame3_label))
button_perform_action3.pack()

delete_button = ttk.Button(
    frame3, text='Delete Database', command=delete_database)
delete_button.pack(pady=10)
frame3_label = ttk.Label(frame3, text='', background='green')
frame3_label.pack()

# List of dropdown menus and frame labels
dropdown_menus = [None, dropdown_menu1, dropdown_menu2, dropdown_menu3]
frame_labels = [None, frame1_label, frame2_label, frame3_label]

# Grid
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)

# Run
window.mainloop()

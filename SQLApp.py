import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import sqlite3

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Get a list of databases in the current directory
databases = [f.replace(".db", "") for f in os.listdir(
    current_directory) if f.endswith('.db')]

# Window
window = tk.Tk()
window.title('Window of widgets')
window.geometry('800x500+900+100')
window.attributes('-alpha', 0.8)

# Create a style for ttk frames
style = ttk.Style()
style.configure("My.TFrame", background="grey")

# Frame 0
frame0 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame0.grid(row=0, column=0, sticky='nsew', padx=30, pady=5)


def create_new_database():
    new_database_name = simpledialog.askstring(
        "New Database", "Enter a name for the new database:")
    if new_database_name:
        create_new_database_in_current_directory(new_database_name)
        refresh_dropdowns()
        frame0_label.config(text=f"Database {new_database_name} created")


def create_new_database_in_current_directory(database_name):
    # Create a new SQLite database in the current directory
    db_connection = sqlite3.connect(os.path.join(
        current_directory, f"{database_name}.db"))
    # Enable foreign key support
    db_connection.execute("PRAGMA foreign_keys = ON")
    db_connection.commit()


# Button to create a new database
create_button = ttk.Button(
    frame0, text='Create Database', command=create_new_database)
create_button.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

# Label to display status
frame0_label = ttk.Label(
    frame0, text='Press to create a database.', background='green')
frame0_label.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

# Frame 1
frame1 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame1.grid(row=1, column=0, sticky='nsew', padx=30, pady=5)

frame1_selection = tk.StringVar()
frame1_selection.set("Select Database")
frame1_dropdown = ttk.Combobox(frame1, values=[
                               "Select Database"] + databases, state='readonly', textvariable=frame1_selection)
frame1_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

button_perform_action1 = ttk.Button(frame1, text='Choose Database', command=lambda: frame1_label.config(
    text=f'Selected database: {frame1_selection.get()}'))
button_perform_action1.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
frame1_label = ttk.Label(
    frame1, text='Select database frame1', background='green')
frame1_label.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

# Frame 2
frame2 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame2.grid(row=2, column=0, sticky='nsew', padx=30, pady=5)

frame2_selection = tk.StringVar()
frame2_selection.set("Select Database")
frame2_dropdown = ttk.Combobox(frame2, values=[
                               "Select Database"] + databases, state='readonly', textvariable=frame2_selection)
frame2_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

button_perform_action2 = ttk.Button(frame2, text='Choose Database', command=lambda: frame2_label.config(
    text=f'Selected database: {frame2_selection.get()}'))
button_perform_action2.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
frame2_label = ttk.Label(
    frame2, text='Select database frame2', background='green')
frame2_label.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

# Frame 3
frame3 = ttk.Frame(window, borderwidth=2, relief="groove", style="My.TFrame")
frame3.grid(row=3, column=0, sticky='nsew', padx=30, pady=5)

frame3_selection = tk.StringVar()
frame3_selection.set("Select Database")
frame3_dropdown = ttk.Combobox(frame3, values=[
                               "Select Database"] + databases, state='readonly', textvariable=frame3_selection)
frame3_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

frame3_label = ttk.Label(
    frame3, text='Select database from the dropdown to delete.', background='green')
frame3_label.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)


# Function to refresh dropdowns


def refresh_dropdowns():
    global databases
    databases = [f.replace(".db", "") for f in os.listdir(
        current_directory) if f.endswith('.db')]
    frame1_dropdown['values'] = ["Select Database"] + databases
    frame2_dropdown['values'] = ["Select Database"] + databases
    frame3_dropdown['values'] = ["Select Database"] + databases

# Function to delete a database


def delete_database():
    selected_option = frame3_selection.get()
    if selected_option and selected_option != "Select Database":
        confirmation = messagebox.askyesno(
            "Delete Database", f"Are you sure you want to delete {selected_option} database?")
        if confirmation:
            delete_database_file(selected_option)
            refresh_dropdowns()
            frame3_selection.set("Select Database")  # Reset the selection
            frame3_label.config(text=f"Database {
                                selected_option} deleted. Select another database to delete or exit.")


# Function to delete a database file

def delete_database_file(database_name):
    # Delete the database file
    database_file = os.path.join(current_directory, f"{database_name}.db")
    if os.path.exists(database_file):
        os.remove(database_file)


# Button to delete a database
button_perform_action3 = ttk.Button(
    frame3, text='Delete Database', command=delete_database)
button_perform_action3.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

# Grid
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)

# Run
window.mainloop()

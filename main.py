from textwrap import fill
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog, Toplevel
import os
import sqlite3
from turtle import fillcolor
from tkinter import PhotoImage
from PIL import Image, ImageTk






################################################################################################################################################

def create_main_menu():
    menu_frame = ttk.Frame(window)
    menu_frame.grid(row=0, column=0, sticky='nsew')

    menu_bar = tk.Menu(menu_frame)
    main_menu = tk.Menu(menu_bar, tearoff=0)
    
    main_menu.add_command(label="Manage Databases", command=manage_databases)
    main_menu.add_command(label="Manage Tables", command=manage_tables)
    main_menu.add_command(label="Manage Columns", command=manage_columns)
    main_menu.add_command(label="Manage Content", command=manage_content)
    main_menu.add_separator()
    main_menu.add_command(label="Exit", command=window.destroy)
    
    menu_bar.add_cascade(label="Main", menu=main_menu)
    menu_bar.add_command(label="About", command=create_about_frame)
   
    window.config(menu=menu_bar)

#################################################################################################################################################

def create_about_frame():
    # Destroy any existing frames
    for widget in window.winfo_children():
        widget.destroy()

    # Create main menu
    create_main_menu()

    s = ttk.Style()
    s.configure("Frame1.TFrame", background='white')

    # Create and configure the main frame
    main_frame_about = ttk.Frame(window, borderwidth=2, relief="groove", style="Frame1.TFrame")
    main_frame_about.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    main_frame_about.columnconfigure(0, weight=1)

    # Create a new style for the about frame
    about_frame_style = ttk.Style()
    about_frame_style.configure("AboutFrame.TFrame", background='#FAEBD7')  # Set the background color
    about_label_style = ttk.Style()
    about_label_style.configure("AboutFrame.TLabel", background='#FAEBD7')  # Set the background color

    # Create the about frame using the new style
    about_frame = ttk.Frame(main_frame_about, borderwidth=2, relief="groove", style="AboutFrame.TFrame")
    about_frame.pack(expand=True)

    # Load the original logo image (replace 'path_to_logo.png' with the actual path to your logo)
    original_image = Image.open('data\\logo.png')

    # Resize the image to 200x200
    resized_image = original_image.resize((90, 90))

    # Convert the PIL Image to Tkinter PhotoImage
    logo_image = ImageTk.PhotoImage(resized_image)

    # Create and display the logo
    logo_label = ttk.Label(about_frame, image=logo_image, style="AboutFrame.TLabel")
    logo_label.image = logo_image  # to prevent garbage collection
    logo_label.pack(pady=10)

    # Create and display the text with transparent background
    about_text = "Free soft\nDeveloped for all\nAPK_soft\n2024"
    text_label = ttk.Label(about_frame, text=about_text, wraplength=300, justify='center', compound='top', style="AboutFrame.TLabel")
    text_label.pack(pady=10)
    
######################################################################################################################################################    

def manage_databases():
    for widget in window.winfo_children():
        widget.destroy()

    create_main_menu()

    s = ttk.Style()
    s.configure("Frame1.TFrame", background='grey')

    masterframe_1A = ttk.Frame(window, borderwidth=2,relief="groove", style="Frame1.TFrame")
    masterframe_1A.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    masterframe_1A.columnconfigure(0, weight=1)

    contentframe_1A = ttk.Frame(masterframe_1A, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_1A.grid(row=1, column=0, sticky='ew', padx=30, pady=5)

    button_create_database = ttk.Button(contentframe_1A, text='Create Database', command=create_database)
    button_create_database.grid(row=0, column=0, sticky='w', padx=5, pady=5)

    label_1A = ttk.Label(contentframe_1A, text='Press to create a database.', background='#7BCCB5')
    label_1A.grid(row=0, column=1, sticky='w', padx=5, pady=5)

    contentframe_2A = ttk.Frame(masterframe_1A, borderwidth=2,relief="groove", style="My.TFrame")
    contentframe_2A.grid(row=2, column=0, sticky='nsew', padx=30, pady=5)

    # Define contentframe_2A_selection and contentframe_2A_dropdown in the global scope
    global contentframe_2A_selection, contentframe_2A_dropdown
    contentframe_2A_selection = tk.StringVar()
    contentframe_2A_selection.set("Select Database")
    contentframe_2A_dropdown = ttk.Combobox(contentframe_2A, values=["Select Database"] + get_databases(), state='readonly', textvariable=contentframe_2A_selection)
    contentframe_2A_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    label_2A = ttk.Label(contentframe_2A, text='Select database from the dropdown to delete.', background='#7BCCB5')
    label_2A.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

    button_delete_database_2A = ttk.Button(contentframe_2A, text='Delete Database', command=lambda: delete_database(contentframe_2A_dropdown))
    button_delete_database_2A.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    contentframe_3A = ttk.Frame(masterframe_1A, borderwidth=2, relief="groove", style="My.TFrame")

    contentframe_3A.grid(row=3, column=0, sticky='nsew', padx=30, pady=5)

    label_3A = ttk.Label(contentframe_3A, text='All databases in the folder', background='#7BCCB5')
    label_3A.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    frame_database_list = ttk.Frame(contentframe_3A, borderwidth=2, relief="groove", style="My.TFrame")
    frame_database_list.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

    global label_database_list
    label_database_list = ttk.Label(frame_database_list, text='\n'.join(get_databases()), background='white')
    label_database_list.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

def refresh_databases():
    databases = get_databases()
    updated_values = ["Select New Database"] + databases

    # Update the contentframe_2A_dropdown with the latest list of databases
    contentframe_2A_dropdown['values'] = updated_values
    

    # Update the label_database_list with the latest list of databases
    label_database_list.config(text='\n'.join(databases))


def update_database_list_label():
    label_database_list.config(text='\n'.join(get_databases()))

def get_databases():
    return [f.replace(".db", "") for f in os.listdir(current_directory) if f.endswith('.db')]

def create_database():
    new_database_name = simpledialog.askstring(
        "Create Database", "Enter a name for the new database:")
    if new_database_name:
        connection_1 = None  # Initialize the connection_1 variable

        try:
            connection_1 = sqlite3.connect(os.path.join(
                current_directory, f"{new_database_name}.db"))
            messagebox.showinfo("Success", f"Database '{
                                new_database_name}.db' created successfully.")
            refresh_databases()
            update_database_list_label()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error creating database: {e}")
        finally:
            if connection_1:
                connection_1.close()
        update_database_list_label()



def delete_database(frame_dropdown):
    selected_database = contentframe_2A_selection.get()
    if selected_database != "Select New Database":
        confirm_delete = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete {selected_database}.db?")
        if confirm_delete:
            try:
                os.remove(os.path.join(current_directory,
                                       f"{selected_database}.db"))
                messagebox.showinfo("Success", f"Database '{
                                    selected_database}.db' deleted successfully.")
                refresh_databases()

                # Reset the selection to "Select New Database"
                contentframe_2A_selection.set("Select New Database")

                # Update the dropdown in frame1
                frame_dropdown['values'] = [
                    "Select New Database"] + get_databases()

            except Exception as e:
                messagebox.showerror("Error", f"Error deleting database: {e}")
        update_database_list_label()

    
####################################################################################################################################################


def manage_tables():
    
    s = ttk.Style()
    s.configure("Frame1.TFrame", background='grey')
    
    masterframe_1B = ttk.Frame(window, borderwidth=2,
                               relief="groove", style="Frame1.TFrame")
    masterframe_1B.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    masterframe_1B.columnconfigure(0, weight=1)

    contentframe_1B = ttk.Frame(masterframe_1B, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_1B.grid(row=1, column=0, sticky='ew', padx=30, pady=5)
    contentframe_2B = ttk.Frame(masterframe_1B, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_2B.grid(row=2, column=0, sticky='ew', padx=30, pady=5)
    contentframe_3B = ttk.Frame(masterframe_1B, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_3B.grid(row=3, column=0, sticky='ew', padx=30, pady=5)
    
    global contentframe_1B_selection, contentframe_1B_dropdown
    contentframe_1B_selection = tk.StringVar()
    contentframe_1B_selection.set("Select Database")
    contentframe_1B_dropdown = ttk.Combobox(contentframe_1B, values=["Select Database"] + get_databases(), state='readonly', textvariable=contentframe_1B_selection)
    contentframe_1B_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    label_1B = ttk.Label(contentframe_1B, text='Select database from the dropdown menu', background='#7BCCB5')
    label_1B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    
    def create_table():
        selected_database = contentframe_1B_selection.get()

        if selected_database != "Select Database":
            new_table_name = tk.simpledialog.askstring(
                "Create Table", f"Enter a name for the new table in '{selected_database}' database:")
            if new_table_name:
                connection_2 = None  # Initialize the connection_2 variable

                try:
                    connection_2 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                    cursor = connection_2.cursor()

                    # Create the table with a sample column (you can modify this according to your requirements)
                    cursor.execute(f"CREATE TABLE {new_table_name} (id INTEGER PRIMARY KEY, name TEXT);")

                    connection_2.commit()
                    messagebox.showinfo("Success", f"Table '{new_table_name}' created successfully.")
                    refresh_tables(selected_database)

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error creating table: {e}")

                finally:
                    if connection_2:
                        connection_2.close()

    
    label_2B = ttk.Label(contentframe_2B, text='Create table for the selected database or go to the frame below to manage exisiting tables', background='#7BCCB5')
    label_2B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    button_2B = ttk.Button(contentframe_2B, text='Create table', command=create_table)
    button_2B.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    def get_tables(database_name):
        connection_3 = None  # Initialize the connection_3 variable

        try:
            connection_3 = sqlite3.connect(os.path.join(
                current_directory, f"{database_name}.db"))
            cursor = connection_3.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error accessing tables: {e}")
        finally:
            if connection_3:
                connection_3.close()
    
    def update_table_dropdown(event):
        selected_database = contentframe_1B_selection.get()
        if selected_database != "Select Database":
            tables = get_tables(selected_database)
            updated_values = ["Select Table"] + tables
            contentframe_3B_dropdown['values'] = updated_values
            contentframe_3B_selection.set("Select Table")

    

    def rename_table():
        selected_database = contentframe_1B_selection.get()
        selected_table = contentframe_3B_selection.get()

        if selected_database != "Select Database" and selected_table != "Select Table":
            new_table_name = tk.simpledialog.askstring(
                "Rename Table", f"Enter a new name for '{selected_table}' in '{selected_database}' database:")
            if new_table_name:
                connection_4 = None  # Initialize the connection_4 variable

                try:
                    connection_4 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                    cursor = connection_4.cursor()

                    # Rename the table using ALTER TABLE statement
                    cursor.execute(f"ALTER TABLE {selected_table} RENAME TO {new_table_name};")

                    connection_4.commit()
                    messagebox.showinfo("Success", f"Table '{selected_table}' renamed to '{new_table_name}' successfully.")
                    refresh_tables(selected_database)

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error renaming table: {e}")

                finally:
                    if connection_4:
                        connection_4.close()




    contentframe_1B_dropdown.bind("<<ComboboxSelected>>", update_table_dropdown)

    def refresh_tables(database_name):
        tables = get_tables(database_name)
        updated_values = ["Select Table"] + tables

        # Update the contentframe_3B_dropdown with the latest list of tables
        contentframe_3B_dropdown['values'] = updated_values
        contentframe_3B_selection.set("Select Table")



    def delete_table():
        selected_database = contentframe_1B_selection.get()
        selected_table = contentframe_3B_selection.get()

        if selected_database != "Select Database" and selected_table != "Select Table":
            confirm_delete = messagebox.askyesno(
                "Confirm Delete", f"Are you sure you want to delete the table '{selected_table}' in '{selected_database}' database?")
            if confirm_delete:
                connection_5 = None  # Initialize the connection_5 variable

                try:
                    connection_5 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                    cursor = connection_5.cursor()

                    # Delete the table using the DROP TABLE statement
                    cursor.execute(f"DROP TABLE {selected_table};")

                    connection_5.commit()
                    messagebox.showinfo("Success", f"Table '{selected_table}' deleted successfully.")
                    refresh_tables(selected_database)

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error deleting table: {e}")

                finally:
                    if connection_5:
                        connection_5.close()

    
    def clear_table_content():
        selected_database = contentframe_1B_selection.get()
        selected_table = contentframe_3B_selection.get()

        if selected_database != "Select Database" and selected_table != "Select Table":
            confirm_clear = messagebox.askyesno(
                "Confirm Clear", f"Are you sure you want to clear all content from the table '{selected_table}' in '{selected_database}' database?")
            if confirm_clear:
                connection_6 = None  # Initialize the connection_6 variable

                try:
                    connection_6 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                    cursor = connection_6.cursor()

                    # Clear all content from the table using DELETE statement
                    cursor.execute(f"DELETE FROM {selected_table};")

                    connection_6.commit()
                    messagebox.showinfo("Success", f"All content from the table '{selected_table}' cleared successfully.")

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error clearing table content: {e}")

                finally:
                    if connection_6:
                        connection_6.close()

    
    def delete_all_columns_except_id():
        selected_database = contentframe_1B_selection.get()
        selected_table = contentframe_3B_selection.get()

        if selected_database != "Select Database" and selected_table != "Select Table":
            confirm_delete = messagebox.askyesno(
                "Confirm Delete", f"Are you sure you want to delete all columns (except 'id') in the table '{selected_table}' including all content in '{selected_database}' database?")
            if confirm_delete:
                connection_7 = None  # Initialize the connection_7 variable

                try:
                    connection_7 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                    cursor = connection_7.cursor()

                    # Get the list of columns in the table
                    cursor.execute(f"PRAGMA table_info({selected_table});")
                    columns = cursor.fetchall()

                    # Construct the ALTER TABLE statement to drop each column (except 'id')
                    for column in columns:
                        column_name = column[1]
                        if column_name.lower() != 'id':
                            cursor.execute(f"ALTER TABLE {selected_table} DROP COLUMN {column_name};")

                    connection_7.commit()
                    messagebox.showinfo("Success", f"All columns (except 'id') in the table '{selected_table}' deleted successfully.")
                    refresh_tables(selected_database)

                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error deleting all columns in the table: {e}")

                finally:
                    if connection_7:
                        connection_7.close()

    
    global contentframe_3B_selection, contentframe_3B_dropdown
    contentframe_3B_selection = tk.StringVar()
    contentframe_3B_selection.set("Select Tables")
    contentframe_3B_dropdown = ttk.Combobox(contentframe_3B, values=["Select Table"] + get_databases(), state='readonly', textvariable=contentframe_3B_selection)
    contentframe_3B_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)    
    label_3B_main = ttk.Label(contentframe_3B, text='Choose tables from the selected database to manage', background='#7BCCB5')
    label_3B_main.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    button_3B_1 = ttk.Button(contentframe_3B, text='Rename table', command=rename_table)
    button_3B_1.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    label_3B_1 = ttk.Label(contentframe_3B, text='Press to rename the table', background='#7BCCB5')
    label_3B_1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    button_3B_2 = ttk.Button(contentframe_3B, text='Delete table', command=delete_table)
    button_3B_2.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
    label_3B_2 = ttk.Label(contentframe_3B, text='Press to delete the table', background='#7BCCB5')
    label_3B_2.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    button_3B_3 = ttk.Button(contentframe_3B, text='Clear table content', command=clear_table_content)
    button_3B_3.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
    label_3B_3 = ttk.Label(contentframe_3B, text='Press to clear table content', background='#7BCCB5')
    label_3B_3.grid(row=3, column=1, sticky='nsew', padx=5, pady=5)
    button_3B_4 = ttk.Button(contentframe_3B, text='Delete all columns', command=delete_all_columns_except_id)
    button_3B_4.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)
    label_3B_4 = ttk.Label(contentframe_3B, text="Press to delete all columns in the table (except 'id')", background='#7BCCB5')
    label_3B_4.grid(row=4, column=1, sticky='nsew', padx=5, pady=5)

########################################################################################################################################################

def manage_columns():
    for widget in window.winfo_children():
        widget.destroy()

    create_main_menu()

    s = ttk.Style()
    s.configure("Frame1.TFrame", background='grey')

    masterframe_1C = ttk.Frame(window, borderwidth=2, relief="groove", style="Frame1.TFrame")
    masterframe_1C.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    masterframe_1C.columnconfigure(0, weight=1)

    contentframe_1C = ttk.Frame(masterframe_1C, borderwidth=2, relief="groove", style="My.TFrame", width=1)
    contentframe_1C.grid(row=1, column=0, sticky='ew', padx=30, pady=5)

    contentframe_2C = ttk.Frame(masterframe_1C, borderwidth=2, relief="groove", style="My.TFrame", width=1)
    contentframe_2C.grid(row=2, column=0, sticky='ew', padx=30, pady=5)

    contentframe_3C = ttk.Frame(masterframe_1C, borderwidth=2, relief="groove", style="My.TFrame", width=1)
    contentframe_3C.grid(row=3, column=0, sticky='ew', padx=30, pady=5)

    global contentframe_1C_selection, contentframe_1C_dropdown
    contentframe_1C_selection = tk.StringVar()
    contentframe_1C_selection.set("Select Database")
    contentframe_1C_dropdown = ttk.Combobox(contentframe_1C, values=["Select Database"] + get_databases(), state='readonly', textvariable=contentframe_1C_selection)
    contentframe_1C_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    label_1C = ttk.Label(contentframe_1C, text='Select database from the dropdown menu', background='#7BCCB5')
    label_1C.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    def update_table_dropdown(event):
        selected_database = contentframe_1C_selection.get()
        if selected_database != "Select Database":
            tables = get_tables_col(selected_database)                                  ################################################################!!!!!!#################################################
            updated_values = ["Select Table"] + tables
            contentframe_2C_dropdown['values'] = updated_values
            contentframe_2C_selection.set("Select Table")

    contentframe_1C_dropdown.bind("<<ComboboxSelected>>", update_table_dropdown)

    global contentframe_2C_selection, contentframe_2C_dropdown
    contentframe_2C_selection = tk.StringVar()
    contentframe_2C_selection.set("Select Table")
    contentframe_2C_dropdown = ttk.Combobox(contentframe_2C, values=["Select Table"], state='readonly', textvariable=contentframe_2C_selection)
    contentframe_2C_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

    label_2C = ttk.Label(contentframe_2C, text='Select table from the dropdown menu', background='#7BCCB5')
    label_2C.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    def update_column_dropdown(event):
        selected_table = contentframe_2C_selection.get()
        selected_database = contentframe_1C_selection.get()

        if selected_table != "Select Table" and selected_database != "Select Database":
            columns = get_columns_col(selected_database, selected_table)
            updated_values = ["Select Column"] + columns
            contentframe_3C_dropdown['values'] = updated_values
            contentframe_3C_selection.set("Select Column")

    contentframe_2C_dropdown.bind("<<ComboboxSelected>>", update_column_dropdown)

    global contentframe_3C_selection, contentframe_3C_dropdown
    
    button_3C_main = ttk.Button(contentframe_3C, text='Show all columns & types', command=lambda: show_all_columns_and_types(contentframe_1C_selection.get(), contentframe_2C_selection.get()))
    button_3C_main.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    label_3C_main = ttk.Label(contentframe_3C, text='Press to display all columns and types from selected table', background='#7BCCB5')
    label_3C_main.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    
    
    
    contentframe_3C_selection = tk.StringVar()
    contentframe_3C_selection.set("Select Column")
    contentframe_3C_dropdown = ttk.Combobox(contentframe_3C, values=["Select Column"], state='readonly', textvariable=contentframe_3C_selection)
    contentframe_3C_dropdown.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    label_3C_1 = ttk.Label(contentframe_3C, text='Choose column from the selected table to manage or: ->', background='#7BCCB5')
    label_3C_1.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    button_3C_1 = ttk.Button(contentframe_3C, text='Create column', command=lambda: create_column(contentframe_1C_selection.get(), contentframe_2C_selection.get()))
    button_3C_1.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)

    button_3C_2 = ttk.Button(contentframe_3C, text='Rename column', command=lambda: on_rename_column(contentframe_1C_selection.get(), contentframe_2C_selection.get()))
    button_3C_2.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
    label_3C_2 = ttk.Label(contentframe_3C, text='Press to rename the column', background='#7BCCB5')
    label_3C_2.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
   
    button_3C_3 = ttk.Button(contentframe_3C, text='Change column type', command=lambda: on_change_column_type(contentframe_1C_selection.get(), contentframe_2C_selection.get()))
    button_3C_3.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
    label_3C_3 = ttk.Label(contentframe_3C, text='Press to change the column type', background='#7BCCB5')
    label_3C_3.grid(row=3, column=1, sticky='nsew', padx=5, pady=5)

    button_3C_4 = ttk.Button(contentframe_3C, text='Clear column content', command=lambda: on_clear_column_content(contentframe_1C_selection.get(), contentframe_2C_selection.get()))
    button_3C_4.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)
    label_3C_4 = ttk.Label(contentframe_3C, text='Press to clear the content of the selected column', background='#7BCCB5')
    label_3C_4.grid(row=4, column=1, sticky='nsew', padx=5, pady=5)

    button_3C_5 = ttk.Button(contentframe_3C, text='Delete column', command=lambda: on_delete_column(contentframe_1C_selection.get(), contentframe_2C_selection.get()))
    button_3C_5.grid(row=5, column=0, sticky='nsew', padx=5, pady=5)
    label_3C_5 = ttk.Label(contentframe_3C, text='Press to delete the column', background='#7BCCB5')
    label_3C_5.grid(row=5, column=1, sticky='nsew', padx=5, pady=5)

    

def get_columns_col(database_name, table_name):
    connection_9 = None  # Initialize the connection_9 variable

    try:
        connection_9 = sqlite3.connect(os.path.join(current_directory, f"{database_name}.db"))
        cursor = connection_9.cursor()

        # Fetch column names from the specified table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Extract column names from the result
        column_names = [column[1] for column in columns]

        return column_names
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching columns: {e}")
    finally:
        if connection_9:
            connection_9.close()

def get_tables_col(database_name):
    connection_9_1 = None  # Initialize the connection_9_1 variable

    try:
        connection_9_1 = sqlite3.connect(os.path.join(
            current_directory, f"{database_name}.db"))
        cursor = connection_9_1.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing tables: {e}")
    finally:
        if connection_9_1:
            connection_9_1.close()

def create_column(selected_database, selected_table):
    def on_create_column():
        column_name = column_name_entry.get()
        if column_name:
            data_type = data_type_combobox.get()

            connection_8 = None
            try:
                connection_8 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                cursor = connection_8.cursor()

                # Execute the SQL statement to add a column
                cursor.execute(f"ALTER TABLE {selected_table} ADD COLUMN {column_name} {data_type};")
                connection_8.commit()

                # Inform the user that the column has been created
                messagebox.showinfo("Success", f"Column '{column_name}' created successfully!")

                # Fetch and print the updated columns
                updated_columns = get_columns_col(selected_database, selected_table)

                # Update the values in contentframe_3C_dropdown
                updated_values = ["Select Column"] + updated_columns
                contentframe_3C_dropdown['values'] = updated_values
                contentframe_3C_selection.set("Select Column")

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error creating column: {e}")
            finally:
                if connection_8 is not None:
                    connection_8.close()

            popup.destroy()


    popup = Toplevel()
    popup.title("Create Column")

    # Entry for column name
    ttk.Label(popup, text="Column Name:").grid(row=0, column=0, padx=5, pady=5)
    column_name_entry = ttk.Entry(popup)
    column_name_entry.grid(row=0, column=1, padx=5, pady=5)

    # Combo box for data types
    ttk.Label(popup, text="Data Type:").grid(row=1, column=0, padx=5, pady=5)
    data_types = ["TEXT", "INTEGER", "REAL", "DECIMAL", "BOOLEAN", "FLOAT"]
    data_type_combobox = ttk.Combobox(popup, values=data_types, state="readonly")
    data_type_combobox.set(data_types[0])
    data_type_combobox.grid(row=1, column=1, padx=5, pady=5)

    # Button to create column
    ttk.Button(popup, text="Create Column", command=on_create_column).grid(row=2, column=0, columnspan=2, pady=10)

    # Focus on the entry field when the popup is opened
    column_name_entry.focus_set()

    popup.transient()
    popup.grab_set()
    popup.wait_window()


def on_rename_column(selected_database, selected_table):
    selected_column = contentframe_3C_selection.get()
    if selected_column != "Select Column":
        new_column_name = simpledialog.askstring("Rename Column", f"Enter new name for column '{selected_column}':")

        if new_column_name:
            connection_10 = None
            try:
                connection_10 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                cursor = connection_10.cursor()

                # Execute the SQL statement to rename the column
                cursor.execute(f"ALTER TABLE {selected_table} RENAME COLUMN {selected_column} TO {new_column_name};")
                connection_10.commit()

                # Inform the user that the column has been renamed
                messagebox.showinfo("Success", f"Column '{selected_column}' renamed to '{new_column_name}' successfully!")

                # Fetch and print the updated columns
                updated_columns = get_columns_col(selected_database, selected_table)

                # Update the values in contentframe_3C_dropdown
                updated_values = ["Select Column"] + updated_columns
                contentframe_3C_dropdown['values'] = updated_values
                contentframe_3C_selection.set("Select Column")

            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error renaming column: {e}")
            finally:
                if connection_10 is not None:
                    connection_10.close()

def on_delete_column(selected_database, selected_table):
    selected_column = contentframe_3C_selection.get()

    if selected_column != "Select Column":
        connection_11 = None  # Initialize the connection_11 variable

        try:
            connection_11 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
            cursor = connection_11.cursor()

            # Execute the SQL statement to delete the column
            cursor.execute(f"ALTER TABLE {selected_table} DROP COLUMN {selected_column};")
            connection_11.commit()

            # Inform the user that the column has been deleted
            messagebox.showinfo("Success", f"Column '{selected_column}' deleted successfully!")

            # Fetch and print the updated columns
            update_column_dropdown(selected_database, selected_table)
            updated_columns = get_columns_col(selected_database, selected_table)
            print(updated_columns)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting column: {e}")

        finally:
            if connection_11:
                connection_11.close()


def update_column_dropdown(selected_database, selected_table):
    columns = get_columns_col(selected_database, selected_table)
    updated_values = ["Select Column"] + columns
    contentframe_3C_dropdown['values'] = updated_values
    contentframe_3C_selection.set("Select Column")
        
def on_change_column_type(selected_database, selected_table):
    selected_column = contentframe_3C_selection.get()

    if selected_column != "Select Column":
        # Create data_types inside the function
        data_types = ["TEXT", "INTEGER", "REAL", "DECIMAL", "BOOLEAN", "FLOAT"]
        connection_12 = None
        try:
            # Create the data types dropdown in a popup window
            popup = tk.Toplevel(window)
            popup.title("Change Column Type")

            ttk.Label(popup, text="Data Type:").grid(row=1, column=0, padx=5, pady=5)
            data_type_combobox = ttk.Combobox(popup, values=data_types, state="readonly")
            data_type_combobox.set(data_types[0])
            data_type_combobox.grid(row=1, column=1, padx=5, pady=5)

            def on_confirm():
                new_data_type = data_type_combobox.get()

                if new_data_type:
                    connection_12 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
                    cursor = connection_12.cursor()

                    # Execute the SQL statement to change the column type
                    cursor.execute(f"PRAGMA foreign_keys=off;")
                    cursor.execute(f"BEGIN TRANSACTION;")
                    cursor.execute(f"CREATE TEMPORARY TABLE backup({', '.join(get_columns_col(selected_database, selected_table))});")
                    cursor.execute(f"INSERT INTO backup SELECT * FROM {selected_table};")
                    cursor.execute(f"DROP TABLE {selected_table};")
                    cursor.execute(f"CREATE TABLE {selected_table}({', '.join(get_columns_col(selected_database, selected_table)).replace(selected_column, f'{selected_column} {new_data_type}')});")
                    cursor.execute(f"INSERT INTO {selected_table} SELECT * FROM backup;")
                    cursor.execute(f"DROP TABLE backup;")
                    cursor.execute(f"COMMIT;")

                    connection_12.commit()

                    # Inform the user that the column type has been changed
                    messagebox.showinfo("Success", f"Column type for '{selected_column}' changed to '{new_data_type}' successfully!")

                    # Fetch and print the updated columns
                    update_column_dropdown(selected_database, selected_table)
                    updated_columns = get_columns_col(selected_database, selected_table)
                    print(updated_columns)

                    popup.destroy()

            ttk.Button(popup, text="Confirm", command=on_confirm).grid(row=2, column=0, columnspan=2, pady=10)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error changing column type: {e}")
        finally:
            if connection_12:
                connection_12.close()
                    
def on_clear_column_content(selected_database, selected_table):
    selected_column = contentframe_3C_selection.get()

    if selected_column != "Select Column":
        connection_13 = None  # Initialize the connection_13 variable

        try:
            connection_13 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
            cursor = connection_13.cursor()

            # Execute the SQL statement to clear the content of the selected column
            cursor.execute(f"UPDATE {selected_table} SET {selected_column} = NULL;")

            connection_13.commit()

            # Inform the user that the content has been cleared
            messagebox.showinfo("Success", f"Content of column '{selected_column}' cleared successfully!")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error clearing column content: {e}")

        finally:
            if connection_13:
                connection_13.close()
                    
def show_all_columns_and_types(selected_database, selected_table):
    connection_14 = None  # Initialize connection_14 outside the try block
    
    try:
        connection_14 = sqlite3.connect(os.path.join(current_directory, f"{selected_database}.db"))
        cursor = connection_14.cursor()

        # Fetch column names and types from the specified table
        cursor.execute(f"PRAGMA table_info({selected_table});")
        columns_info = cursor.fetchall()

        # Create a popup window to display the information
        popup = tk.Toplevel(window)
        popup.title("Columns and Types")
        
        # Create a Treeview widget for displaying the information
        columns_tree = ttk.Treeview(popup)
        columns_tree["columns"] = ("Column Name", "Type")
        columns_tree.heading("#0", text="Index")
        columns_tree.column("#0", width=50)
        columns_tree.heading("Column Name", text="Column Name")
        columns_tree.column("Column Name", width=150)
        columns_tree.heading("Type", text="Type")
        columns_tree.column("Type", width=100)

        # Insert data into the Treeview
        for index, column_info in enumerate(columns_info, 1):
            column_name = column_info[1]
            column_type = column_info[2]
            columns_tree.insert("", str(index), text=str(index), values=(column_name, column_type))


        columns_tree.pack(padx=10, pady=10)
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error fetching columns and types: {e}")
    finally:
        if connection_14:
            connection_14.close()


    
####################################################################################################################################

current_directory_mc = os.getcwd()
current_database_mc = None  # Make sure to set these values appropriately in your code
current_table_mc = None

def manage_content():
    for widget in window.winfo_children():
        widget.destroy()

    create_main_menu()

    s = ttk.Style()
    s.configure("Frame1.TFrame", background='grey')
    
    masterframe_1D = ttk.Frame(window, borderwidth=2,relief="groove", style="Frame1.TFrame")
    masterframe_1D.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    masterframe_1D.columnconfigure(0, weight=1)

    contentframe_1D = ttk.Frame(masterframe_1D, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_1D.grid(row=1, column=0, sticky='ew', padx=30, pady=5)
    contentframe_2D = ttk.Frame(masterframe_1D, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_2D.grid(row=2, column=0, sticky='ew', padx=30, pady=5)
    contentframe_3D = ttk.Frame(masterframe_1D, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_3D.grid(row=3, column=0, sticky='ew', padx=30, pady=5)



    global contentframe_1D_dropdown_database
    global contentframe_1D_dropdown_table
    global contentframe_1D_selection_database
    global contentframe_1D_selection_table
         
    contentframe_1D_selection_database = tk.StringVar()
    contentframe_1D_selection_database.set("Select Database")
    contentframe_1D_dropdown_database = ttk.Combobox(contentframe_1D, values=["Select Database"] + get_databases_cm(), state='readonly', textvariable=contentframe_1D_selection_database)
    contentframe_1D_dropdown_database.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    contentframe_1D_dropdown_database.bind("<<ComboboxSelected>>", content_update_tables)
 
    contentframe_1D_selection_table = tk.StringVar()
    contentframe_1D_selection_table.set("Select Table")   
    contentframe_1D_dropdown_table = ttk.Combobox(contentframe_1D, values=["Select Table"]+get_tables_cm(contentframe_1D_selection_database), state='readonly', textvariable=contentframe_1D_selection_table)
    contentframe_1D_dropdown_table.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    label_1D = ttk.Label(contentframe_1D, text='Select database and table where to perform an upload', background='#7DCCD5')
    label_1D.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)



    button_2D_1 = ttk.Button(contentframe_2D, text='Choose one file to upload', command=lambda: upload_file_dialog(contentframe_1D_selection_database.get(), contentframe_1D_selection_table.get()))
    button_2D_1.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    label_2D_1 = ttk.Label(contentframe_2D, text='Select database and table where to perform an upload', background='#7DCCD5')
    label_2D_1.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    button_2D_2 = ttk.Button(contentframe_2D, text='Choose folder to upload', command=lambda: print("Tables!"))
    button_2D_2.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    label_2D_2 = ttk.Label(contentframe_2D, text='Select database and table where to perform an upload', background='#7DCCD5')
    label_2D_2.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

    label_3D = ttk.Label(contentframe_3D, text='Result of the upload:', background='#7DCCD5')
    label_3D.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

def upload_file_dialog(selected_database, selected_table):
    if selected_database == "Select Database" or selected_table == "Select Table":
        messagebox.showerror("Error", "Please select a database and table.")
        return

    popup = Toplevel()
    popup.title("Upload File")

    masterframe_popup = ttk.Frame(popup, borderwidth=2,
                               relief="groove", style="Frame1.TFrame")
    masterframe_popup.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    masterframe_popup.columnconfigure(0, weight=1)
    
    contentframe_popup = ttk.Frame(masterframe_popup, borderwidth=2,relief="groove", style="My.TFrame", width=1)
    contentframe_popup.grid(row=1, column=0, sticky='ew', padx=30, pady=5)

    columns_label = ttk.Label(contentframe_popup, text="Select column for file content:")
    columns_label.grid(row=0, column=0, padx=10, pady=10)

    file_content_dropdown = ttk.Combobox(contentframe_popup, values=get_table_columns(selected_table), state='readonly')
    file_content_dropdown.grid(row=0, column=1, padx=10, pady=10)

    file_name_label = ttk.Label(contentframe_popup, text="Select column for file name:")
    file_name_label.grid(row=1, column=0, padx=10, pady=10)

    file_name_dropdown = ttk.Combobox(contentframe_popup, values=get_table_columns(selected_table), state='readonly')
    file_name_dropdown.grid(row=1, column=1, padx=10, pady=10)

    browse_button = ttk.Button(contentframe_popup, text="Browse", command=lambda: browse_file(file_content_dropdown, file_name_dropdown))
    browse_button.grid(row=2, column=0, columnspan=2, pady=10)

    submit_button = ttk.Button(contentframe_popup, text="Submit", command=lambda: submit_upload(selected_database, selected_table, file_content_dropdown.get(), file_name_dropdown.get()))
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)

def browse_file(file_content_dropdown, file_name_dropdown):
    file_path = filedialog.askopenfilename(title="Select a file to upload")
    if file_path:
        # Perform any additional actions here if needed
        pass

def submit_upload(selected_database, selected_table, file_content_column, file_name_column):
    # Implement the file upload logic here
    # Use the provided parameters to handle the file upload to the selected table
    # For demonstration, let's print the selected values.
    print("Selected Database:", selected_database)
    print("Selected Table:", selected_table)
    print("File Content Column:", file_content_column)
    print("File Name Column:", file_name_column)
    messagebox.showinfo("Upload Complete", "File uploaded successfully!")
    # Add further actions if needed

def content_update_tables(event):
    global contentframe_1D_dropdown_table
    global contentframe_1D_selection_database
    selected_database = contentframe_1D_selection_database.get()
    if selected_database != "Select Database":
        tables = get_tables_cm(selected_database)
        contentframe_1D_dropdown_table['values'] = ["Select Table"] + tables
        contentframe_1D_dropdown_table.set("Select Table")

def get_databases_cm():
    current_directory = os.getcwd()
    database_files = [file for file in os.listdir(current_directory) if file.endswith(".db")]
    return database_files

# Replace this function with your actual implementation
# Replace this function with your actual implementation
def get_tables_cm(database):
    current_directory = os.getcwd()
    db_path = os.path.join(current_directory, f"{database}.db")

    connection_15 = None  # Initialize connection_15 outside the try block

    try:
        connection_15 = sqlite3.connect(db_path)
        cursor = connection_15.cursor()

        # Fetch all table names from the SQLite master table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [table[0] for table in cursor.fetchall()]

        return tables

    except sqlite3.Error as e:
        # Handle the error, you can print or log the error message
        print(f"Error retrieving tables for database '{database}': {e}")
        return []

    finally:
        if connection_15:
            connection_15.close()


# "connection" is possibly unbound
# Replace this function with your actual implementation
def get_table_columns(table_name):
    return ["Column1", "Column2"]

##############################################################################################################################################
    

current_directory = os.path.dirname(os.path.abspath(__file__))

window = tk.Tk()
window.title('Window of widgets')
window.geometry('800x500+300+100')
window.attributes('-alpha', 0.8)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

create_main_menu()

window.mainloop()

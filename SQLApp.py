from textwrap import fill
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import sqlite3
from turtle import fillcolor


def get_databases():
    return [f.replace(".db", "") for f in os.listdir(current_directory) if f.endswith('.db')]


def get_tables(database_name):
    try:
        connection = sqlite3.connect(os.path.join(
            current_directory, f"{database_name}.db"))
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        return [table[0] for table in tables]
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error accessing tables: {e}")
    finally:
        if connection:
            connection.close()


def create_database():
    new_database_name = simpledialog.askstring(
        "Create Database", "Enter a name for the new database:")
    if new_database_name:
        try:
            connection = sqlite3.connect(os.path.join(
                current_directory, f"{new_database_name}.db"))
            messagebox.showinfo("Success", f"Database '{
                                new_database_name}.db' created successfully.")
            refresh_databases()
            update_database_list_label()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error creating database: {e}")
        finally:
            if connection:
                connection.close()
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

    about_menu = tk.Menu(menu_bar, tearoff=0)
    about_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About", "Your application description goes here."))
    menu_bar.add_cascade(label="About", menu=about_menu)

    window.config(menu=menu_bar)


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

    button_delete_database = ttk.Button(contentframe_2A, text='Delete Database', command=lambda: delete_database(contentframe_2A_dropdown))
    button_delete_database.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

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
    frame1_dropdown['values'] = updated_values

    # Update the label_database_list with the latest list of databases
    label_database_list.config(text='\n'.join(databases))


def update_database_list_label():
    label_database_list.config(text='\n'.join(get_databases()))


def manage_columns():
    for widget in window.winfo_children():
        widget.destroy()

    create_main_menu()

    #####

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
    
    global contentframe_2B_selection, contentframe_2B_dropdown
    contentframe_2B_selection = tk.StringVar()
    contentframe_2B_selection.set("Select Tables")
    contentframe_2B_dropdown = ttk.Combobox(contentframe_2B, values=["Select Database"] + get_databases(), state='readonly', textvariable=contentframe_2B_selection)
    contentframe_2B_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    label_2B = ttk.Label(contentframe_2B, text='Choose tables for the selected database', background='#7BCCB5')
    label_2B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
    button_2B = ttk.Button(contentframe_2B, text='Select table', command=lambda:print('Table ___ selected!'))
    button_2B.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    
    label_3B = ttk.Label(contentframe_3B, text='Columns from the selected table:', background='#7BCCB5')
    label_3B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    


def manage_content():
    for widget in window.winfo_children():
        widget.destroy()

    create_main_menu()

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
    
    global contentframe_2B_selection, contentframe_2B_dropdown
    contentframe_2B_selection = tk.StringVar()
    contentframe_2B_selection.set("Select Tables")
    
    
    button_2B = ttk.Button(contentframe_2B, text='Choose file to upload', command=lambda:print('Table ___ selected!'))
    button_2B.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    contentframe_2B_dropdown = ttk.Combobox(contentframe_2B, values=['table 1','table 2'], state='readonly')
    contentframe_2B_dropdown.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
    
    label_2B = ttk.Label(contentframe_2B, text='Choose table where to place file name', background='#7BCCB5')
    label_2B.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
    
    contentframe_2B_dropdown = ttk.Combobox(contentframe_2B, values=['table 1','table 2'], state='readonly')
    contentframe_2B_dropdown.grid(row=2, column=1, sticky='nsew', padx=5, pady=5)
    
    label_2B = ttk.Label(contentframe_2B, text='Choose table where to place file content', background='#7BCCB5')
    label_2B.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        
    button_2B = ttk.Button(contentframe_2B, text='Upload file to database', command=lambda:print('Table ___ selected!'))
    button_2B.grid(row=3, column=0, sticky='nsew', padx=5, pady=5)
    
    label_3B = ttk.Label(contentframe_3B, text='Result of the upload:', background='#7BCCB5')
    label_3B.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

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
    
    global contentframe_2B_selection, contentframe_2B_dropdown
    contentframe_2B_selection = tk.StringVar()
    contentframe_2B_selection.set("Select Tables")
    contentframe_2B_dropdown = ttk.Combobox(contentframe_2B, values=["Select Database"] + get_databases(), state='readonly', textvariable=contentframe_2B_selection)
    contentframe_2B_dropdown.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    label_2B = ttk.Label(contentframe_2B, text='Choose tables for the selected database', background='#7BCCB5')
    label_2B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
    button_3B = ttk.Button(contentframe_3B, text='Create table', command=lambda:print('Table ___ created!'))
    button_3B.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    button_3B = ttk.Button(contentframe_3B, text='Rename table', command=lambda:print('Table ___ renamed!'))
    button_3B.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    button_3B = ttk.Button(contentframe_3B, text='Delete table', command=lambda:print('Table ___ deleted!'))
    button_3B.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
    
    


current_directory = os.path.dirname(os.path.abspath(__file__))

window = tk.Tk()
window.title('Window of widgets')
window.geometry('800x500+900+100')
window.attributes('-alpha', 0.8)

window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

create_main_menu()

window.mainloop()

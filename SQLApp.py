import tkinter as tk
from tkinter import ttk

# ### Window
window = tk.Tk()
window.title('Window of widgest')
window.geometry('800x500+900+100')
window.attributes('-alpha', 0.8)

# widgets
label1 = ttk.Label(window, text='Create Database', background='red')
label2 = ttk.Label(window, text='Manage tables', background='blue')
label3 = ttk.Label(window, text='Clear database', background='grey')


# grid
window.columnconfigure(0,weight=1)
window.rowconfigure(0,weight=1)
window.rowconfigure(1,weight=1)
window.rowconfigure(2,weight=1)

label1.grid(row=0, column=0, sticky='nsew', padx=20, pady=5)
label2.grid(row=1, column=0, sticky='nsew', padx=20, pady=5)
label3.grid(row=2, column=0, sticky='nsew', padx=20, pady=5)



# run
window.mainloop()



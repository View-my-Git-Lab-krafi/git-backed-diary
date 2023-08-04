import tkinter as tk
from tkinter import messagebox

def input_password_using_tkinter():
    root = tk.Tk()
    root.title("Personal Diary")
    root.geometry("400x200")
    root.configure(bg="#f2f2f2")

    custom_font = ("Arial", 14, "bold")

    title_label = tk.Label(root, text="Welcome to Personal Diary", font=("Arial", 18, "bold"), fg="blue", bg="#f2f2f2")
    title_label.pack(pady=10)

    password_label = tk.Label(root, text="Enter Password:", font=custom_font, fg="black", bg="#f2f2f2")
    password_label.pack()

    password_entry = tk.Entry(root, show="*", font=custom_font)
    password_entry.pack(pady=10)

    check_button = tk.Button(root, text="Unlock Diary", font=custom_font, bg="green", fg="white", command=root.quit)
    check_button.pack(pady=10)
    password_entry.focus_set()

    root.bind('<Return>', lambda event: check_button.invoke())

    root.mainloop()
    entered_password = password_entry.get()
    return entered_password
password = input_password_using_tkinter()
print("Entered Password:", password)

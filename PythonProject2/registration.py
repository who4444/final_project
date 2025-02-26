import tkinter as tk
from tkinter import ttk, messagebox


class LibraryLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Login")
        self.root.geometry("800x600")

        # Apply modern style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Roboto", 10), padding=5)
        self.style.configure("TLabel", font=("Roboto", 10))
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TEntry", padding=5)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # User Login Tab
        self.user_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.user_frame, text="User Login")
        self.create_user_login()

        # Admin Login Tab
        self.admin_frame = ttk.Frame(self.notebook, padding=20)
        self.notebook.add(self.admin_frame, text="Admin Login")
        self.create_admin_login()

    def create_user_login(self):
        ttk.Label(self.user_frame, text="User Login", font=("Roboto", 12, "bold")).pack(pady=10)
        ttk.Label(self.user_frame, text="Username:").pack()
        ttk.Entry(self.user_frame).pack(pady=5)

        ttk.Label(self.user_frame, text="Password:").pack()
        ttk.Entry(self.user_frame, show="*").pack(pady=5)

        ttk.Button(self.user_frame, text="Login", command=self.user_login).pack(pady=5)
        ttk.Button(self.user_frame, text="Register", command=self.open_register_screen).pack(pady=5)

    def create_admin_login(self):
        ttk.Label(self.admin_frame, text="Admin Login", font=("Roboto", 12, "bold")).pack(pady=10)
        ttk.Label(self.admin_frame, text="Username:").pack()
        ttk.Entry(self.admin_frame).pack(pady=5)

        ttk.Label(self.admin_frame, text="Password:").pack()
        ttk.Entry(self.admin_frame, show="*").pack(pady=5)

        ttk.Button(self.admin_frame, text="Login", command=self.admin_login).pack(pady=5)

    def admin_login(self):
        messagebox.showinfo("Admin Login", "Admin login screen to be implemented.")

    def user_login(self):
        messagebox.showinfo("User Login", "User login screen to be implemented.")

    def open_register_screen(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("600x500")

        frame = ttk.Frame(register_window, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Register New User", font=("Roboto", 12, "bold")).pack(pady=10)
        ttk.Label(frame, text="Username:").pack()
        ttk.Entry(frame).pack(pady=10)

        ttk.Label(frame, text="Password:").pack()
        ttk.Entry(frame, show="*").pack(pady=5)

        ttk.Label(frame, text="Email:").pack()
        ttk.Entry(frame).pack(pady=5)

        ttk.Button(frame, text="Register", command=lambda: messagebox.showinfo("Success", "Registration Complete!")) \
            .pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryLogin(root)
    root.mainloop()

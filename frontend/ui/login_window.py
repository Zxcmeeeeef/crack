import tkinter as tk
from tkinter import messagebox, ttk
import requests
import json

API_URL = "http://localhost:5000/api"

class LoginWindow:
    def __init__(self, parent, on_success_callback):
        self.parent = parent
        self.on_success_callback = on_success_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        frame = ttk.Frame(self.parent, padding="20")
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ttk.Label(frame, text="CRACK Social Network", font=("Arial", 24, "bold")).pack(pady=20)
        
        ttk.Label(frame, text="Username:").pack(anchor=tk.W)
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack(pady=5)
        
        ttk.Label(frame, text="Password:").pack(anchor=tk.W)
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.pack(pady=5)
        
        ttk.Button(frame, text="Login", command=self.login).pack(pady=10)
        ttk.Button(frame, text="Register", command=self.show_register).pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            response = requests.post(f"{API_URL}/auth/login", json={
                "username": username,
                "password": password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.on_success_callback(data['user'], data['access_token'])
            else:
                messagebox.showerror("Error", response.json().get('error', 'Login failed'))
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def show_register(self):
        register_window = tk.Toplevel(self.parent)
        register_window.title("Register")
        register_window.geometry("400x300")
        
        frame = ttk.Frame(register_window, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Username:").pack(anchor=tk.W)
        username_entry = ttk.Entry(frame, width=30)
        username_entry.pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack(anchor=tk.W)
        email_entry = ttk.Entry(frame, width=30)
        email_entry.pack(pady=5)
        
        ttk.Label(frame, text="Password:").pack(anchor=tk.W)
        password_entry = ttk.Entry(frame, width=30, show="*")
        password_entry.pack(pady=5)
        
        ttk.Label(frame, text="First Name:").pack(anchor=tk.W)
        first_name_entry = ttk.Entry(frame, width=30)
        first_name_entry.pack(pady=5)
        
        def register():
            try:
                response = requests.post(f"{API_URL}/auth/register", json={
                    "username": username_entry.get(),
                    "email": email_entry.get(),
                    "password": password_entry.get(),
                    "first_name": first_name_entry.get()
                })
                
                if response.status_code == 201:
                    data = response.json()
                    self.on_success_callback(data['user'], data['access_token'])
                    register_window.destroy()
                else:
                    messagebox.showerror("Error", response.json().get('error', 'Registration failed'))
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {str(e)}")
        
        ttk.Button(frame, text="Register", command=register).pack(pady=10)

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import threading
import json
from datetime import datetime

API_URL = "https://crack-ajaw.onrender.com/api"

class ChatWindow:
    def __init__(self, parent, user_data, access_token, on_logout_callback):
        self.parent = parent
        self.user_data = user_data
        self.access_token = access_token
        self.on_logout_callback = on_logout_callback
        self.headers = {"Authorization": f"Bearer {access_token}"}
        
        self.current_channel = None
        self.channels = []
        
        self.setup_ui()
        self.load_channels()
    
    def setup_ui(self):
        # Top bar
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text=f"Welcome, {self.user_data['username']}", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        ttk.Button(top_frame, text="Logout", command=self.logout).pack(side=tk.RIGHT)
        
        # Main container
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Sidebar for channels
        sidebar_frame = ttk.LabelFrame(main_frame, text="Channels", width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        
        self.channels_listbox = tk.Listbox(sidebar_frame, height=20)
        self.channels_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.channels_listbox.bind('<<ListboxSelect>>', self.on_channel_select)
        
        ttk.Button(sidebar_frame, text="New Channel", command=self.show_create_channel).pack(pady=5)
        
        # Chat area
        chat_frame = ttk.LabelFrame(main_frame, text="Chat", padding="10")
        chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=20, state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Message input
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X)
        
        self.message_input = ttk.Entry(input_frame)
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        self.message_input.bind('<Return>', lambda e: self.send_message())
        
        ttk.Button(input_frame, text="Send", command=self.send_message).pack(side=tk.LEFT)
    
    def load_channels(self):
        try:
            response = requests.get(f"{API_URL}/channels", headers=self.headers)
            if response.status_code == 200:
                self.channels = response.json()
                self.update_channels_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load channels: {str(e)}")
    
    def update_channels_list(self):
        self.channels_listbox.delete(0, tk.END)
        for channel in self.channels:
            self.channels_listbox.insert(tk.END, channel['name'])
    
    def on_channel_select(self, event):
        selection = self.channels_listbox.curselection()
        if selection:
            self.current_channel = self.channels[selection[0]]
            self.load_messages()
    
    def load_messages(self):
        if not self.current_channel:
            return
        
        try:
            response = requests.get(
                f"{API_URL}/messages/channel/{self.current_channel['id']}",
                headers=self.headers
            )
            if response.status_code == 200:
                data = response.json()
                self.display_messages(data['messages'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load messages: {str(e)}")
    
    def display_messages(self, messages):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        
        for msg in reversed(messages):
            timestamp = msg['created_at'][:16]
            sender = msg['sender']['username']
            content = msg['content']
            
            self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {content}\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self):
        if not self.current_channel:
            messagebox.showwarning("Warning", "Select a channel first")
            return
        
        content = self.message_input.get()
        if not content:
            return
        
        try:
            response = requests.post(
                f"{API_URL}/messages/send",
                headers=self.headers,
                json={
                    "content": content,
                    "channel_id": self.current_channel['id']
                }
            )
            
            if response.status_code == 201:
                self.message_input.delete(0, tk.END)
                self.load_messages()
            else:
                messagebox.showerror("Error", "Failed to send message")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def show_create_channel(self):
        create_window = tk.Toplevel(self.parent)
        create_window.title("Create Channel")
        create_window.geometry("300x200")
        
        frame = ttk.Frame(create_window, padding="15")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Channel Name:").pack(anchor=tk.W)
        name_entry = ttk.Entry(frame, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(frame, text="Description:").pack(anchor=tk.W)
        desc_entry = ttk.Entry(frame, width=30)
        desc_entry.pack(pady=5)
        
        def create():
            try:
                response = requests.post(
                    f"{API_URL}/channels",
                    headers=self.headers,
                    json={
                        "name": name_entry.get(),
                        "description": desc_entry.get()
                    }
                )
                
                if response.status_code == 201:
                    self.load_channels()
                    create_window.destroy()
                    messagebox.showinfo("Success", "Channel created!")
                else:
                    messagebox.showerror("Error", "Failed to create channel")
            except Exception as e:
                messagebox.showerror("Error", f"Connection error: {str(e)}")
        
        ttk.Button(frame, text="Create", command=create).pack(pady=10)
    
    def logout(self):
        try:
            requests.post(f"{API_URL}/auth/logout", headers=self.headers)
        except:
            pass
        self.on_logout_callback()

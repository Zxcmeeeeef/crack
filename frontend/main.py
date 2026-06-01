import tkinter as tk
from tkinter import messagebox
from ui.login_window import LoginWindow
from ui.chat_window import ChatWindow

class CRACKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRACK - Social Network")
        self.root.geometry("900x600")
        self.current_user = None
        self.access_token = None
        
        self.show_login()
    
    def show_login(self):
        self.clear_window()
        self.login_window = LoginWindow(
            self.root,
            self.on_login_success
        )
    
    def on_login_success(self, user_data, access_token):
        self.current_user = user_data
        self.access_token = access_token
        self.show_chat()
    
    def show_chat(self):
        self.clear_window()
        self.chat_window = ChatWindow(
            self.root,
            self.current_user,
            self.access_token,
            self.on_logout
        )
    
    def on_logout(self):
        self.current_user = None
        self.access_token = None
        self.show_login()
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CRACKApp(root)
    root.mainloop()

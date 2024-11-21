from tkinter import messagebox

class ErrorHandler:
    
    @staticmethod
    def show_error(title, message):
        """Display an error message."""
        messagebox.showerror(title, message)
        
    @staticmethod
    def show_warning(title, message):
        """Display a warning message."""
        messagebox.showwarning(title, message)
        
    @staticmethod
    def show_info(title, message):
        """Display an info message."""
        messagebox.showinfo(title, message)
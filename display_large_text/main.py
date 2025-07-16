import tkinter as tk
from tkinter import simpledialog

def main():
    # Create the root window but hide it initially
    root = tk.Tk()
    root.withdraw()

    # Ask the user for input
    user_text = simpledialog.askstring("Input", "Enter the text you want to display:", parent=root)

    if user_text:
        # Create the main application window
        app_window = tk.Toplevel(root)
        app_window.title("Large Text Display")
        app_window.configure(bg="#282c34") # Dark background

        # Center the text
        app_window.grid_rowconfigure(0, weight=1)
        app_window.grid_columnconfigure(0, weight=1)

        # Create a label to display the text
        text_label = tk.Label(
            app_window,
            text=user_text,
            font=("Helvetica", 72, "bold"),
            fg="#FFFFFF",  # White text
            bg="#282c34",  # Dark background
            wraplength=app_window.winfo_screenwidth() - 100 # Wrap text if it's too long
        )
        text_label.grid(padx=20, pady=20)

        # Function to handle window closing
        def on_closing():
            root.destroy()

        app_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()

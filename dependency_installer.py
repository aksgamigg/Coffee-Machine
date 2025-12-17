import sys
import subprocess
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox


class DependencyInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Machine Setup")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Center the window
        self.center_window()

        # Style (Basic Tkinter since we don't have bootstrap yet)
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#e69138"  # A coffee-like orange

        self.root.configure(bg=self.bg_color)

        # --- UI ELEMENTS ---

        # Header
        header_font = ("Segoe UI", 16, "bold")
        self.lbl_title = tk.Label(
            root,
            text="Initial System Setup",
            bg=self.bg_color,
            fg=self.fg_color,
            font=header_font
        )
        self.lbl_title.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Status Label
        self.lbl_status = tk.Label(
            root,
            text="Ready to install...",
            bg=self.bg_color,
            fg="#cccccc",
            font=("Segoe UI", 10)
        )
        self.lbl_status.pack(pady=5)

        # Log Window (Scrolled Text)
        self.log_text = tk.Text(
            root,
            height=10,
            width=55,
            bg="#1e1e1e",
            fg="#00ff00",  # Hacker style terminal green
            font=("Consolas", 9),
            state="disabled"
        )
        self.log_text.pack(pady=10, padx=20)

        # Action Button
        self.btn_action = tk.Button(
            root,
            text="Install Dependencies",
            bg=self.accent_color,
            fg="black",
            font=("Segoe UI", 10, "bold"),
            command=self.start_installation,
            width=20,
            relief="flat"
        )
        self.btn_action.pack(pady=15)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def find_requirements_file(self):
        # Check current directory
        if os.path.exists("requirements.txt"):
            return "requirements.txt"

        # Check one directory up (common in this project structure)
        parent_req = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "requirements.txt")
        if os.path.exists(parent_req):
            return parent_req

        return None

    def start_installation(self):
        self.btn_action.config(state="disabled", text="Installing...")
        self.progress["value"] = 0

        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.install_process, daemon=True)
        thread.start()

    def install_process(self):
        req_file = self.find_requirements_file()

        if not req_file:
            self.log("ERROR: requirements.txt not found!")
            self.lbl_status.config(text="Error: Missing file", fg="red")
            self.btn_action.config(state="normal", text="Retry")
            return

        self.log(f"Found requirements at: {req_file}")

        # Read requirements
        with open(req_file, 'r') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        total = len(packages)
        self.progress["maximum"] = total

        python_exe = sys.executable

        for i, package in enumerate(packages):
            self.lbl_status.config(text=f"Installing {package}...")
            self.log(f"> pip install {package}")

            try:
                # Run pip install
                process = subprocess.Popen(
                    [python_exe, "-m", "pip", "install", package],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )

                # Wait for completion
                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    self.log(f"✔ Successfully installed {package}")
                else:
                    self.log(f"✘ Failed to install {package}")
                    self.log(stderr)

            except Exception as e:
                self.log(f"CRITICAL ERROR: {e}")

            # Update progress
            self.progress["value"] = i + 1
            self.root.update_idletasks()

        self.lbl_status.config(text="Installation Complete!", fg="#00ff00")
        self.log("--- SETUP FINISHED ---")

        # Change button to "Launch App"
        self.btn_action.config(
            text="Launch App",
            state="normal",
            command=self.launch_app,
            bg="#4caf50"  # Green
        )

    def launch_app(self):
        self.log("Preparing to launch application...")

        # 1. Get current directory (Project Root)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_main = os.path.join(current_dir, "main.py")

        if os.path.exists(target_main):
            self.log(f"Launching: {target_main}")
            self.root.destroy()

            # 2. THE FIX: Use Windows 'start' command
            # We use f-string to build the command safely.
            # 'start' = Open new window
            # '/k' = Keep window open after crash
            # quotes "" around paths handles spaces in folder names

            command = f'start "CoffeeMachine" cmd /k "{sys.executable}" "{target_main}"'

            # shell=True is required to use the 'start' command
            subprocess.Popen(command, shell=True, cwd=current_dir)
        else:
            messagebox.showerror("Error", f"Could not find main.py in:\n{current_dir}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DependencyInstaller(root)
    root.mainloop()

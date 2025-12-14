import tkinter as tk
from tkinter import ttk
import sys
import subprocess
import threading

class DependencyInstaller(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Coffee Machine Setup")
        self.geometry("400x350")
        self.resizable(False, False)

        # REQUIREMENTS LIST
        self.requirements = ["ttkbootstrap", "Pillow"]

        # Styling to match your Darkly theme (manually, since we don't have bootstrap yet)
        self.configure(bg="#2b2b2b")
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Dark theme colors for standard widgets
        self.style.configure("TLabel", background="#2b2b2b", foreground="white", font=("Segoe UI", 10))
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), background="#e0a800", foreground="black")
        self.style.map("TButton", background=[("active", "#c69500")])
        self.style.configure("TProgressbar", troughcolor="#444444", background="#e0a800")

        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Header
        header = tk.Label(self, text="Project Setup", font=("Segoe UI", 16, "bold"), bg="#2b2b2b", fg="#e0a800")
        header.pack(pady=20)

        # Status Label
        self.status_label = ttk.Label(self, text="Ready to install dependencies.")
        self.status_label.pack(pady=5)

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        # Log Area (Text widget)
        self.log_area = tk.Text(self, height=8, width=45, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9), bd=0)
        self.log_area.pack(pady=10)
        self.log_area.insert(tk.END, "Waiting to start...\n")
        self.log_area.config(state=tk.DISABLED)

        # Install Button
        self.btn_install = ttk.Button(self, text="INSTALL DEPENDENCIES", command=self.start_installation)
        self.btn_install.pack(pady=10)

    def log(self, message):
        """Updates the text area safely"""
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def start_installation(self):
        self.btn_install.config(state=tk.DISABLED)
        self.progress['value'] = 0
        # Run in a separate thread so GUI doesn't freeze
        threading.Thread(target=self.install_process, daemon=True).start()

    def install_process(self):
        total = len(self.requirements)
        step = 100 / total

        for pkg in self.requirements:
            self.status_label.config(text=f"Installing {pkg}...")
            self.log(f"Pip installing: {pkg}")

            try:
                # The actual install command
                subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
                self.log(f"Successfully installed {pkg}")
            except subprocess.CalledProcessError:
                self.log(f"ERROR installing {pkg}")

            self.progress['value'] += step
            self.update_idletasks()

        self.status_label.config(text="Installation Complete!", foreground="#00ff00")
        self.log("All tasks finished.")
        self.btn_install.config(text="LAUNCH APP", command=self.launch_app, state=tk.NORMAL)

    def launch_app(self):
        self.log("Launching main.py...")
        self.destroy()  # Close installer
        # Launch the main app
        subprocess.Popen([sys.executable, "main.py"])


if __name__ == "__main__":
    app = DependencyInstaller()
    app.mainloop()
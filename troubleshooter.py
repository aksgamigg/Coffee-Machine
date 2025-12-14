import tkinter as tk
from tkinter import ttk
import sys
import os
import importlib.util
import subprocess
import threading

# --- CONFIGURATION ---
REQUIRED_LIBS = ["ttkbootstrap", "PIL"]  # PIL is the import name for Pillow

# MAP: Define where each file SHOULD be relative to the project root
# Format: "path/to/folder": ["file1.py", "file2.py"]
FILE_STRUCTURE = {
    ".": ["main.py"],  # Root folder
    "gui": ["gui_code.py"],  # gui folder
    "backend": ["logic.py"]  # backend folder
}

REQUIRED_ASSETS = [
    "logo.ico",
    "StartScreen.png",
    "OrderWindow.png",
    "PaymentWindow.png",
    "ChangeWindow.png",
    "EspressoWindow.png",
    "LatteWindow.png",
    "CappuccinoWindow.png"
]


class CoffeeTroubleshooter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Coffee Machine Diagnostics")
        self.geometry("650x600")  # Made slightly wider for path names
        self.configure(bg="#1e1e1e")

        # Style Configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", background="#1e1e1e", foreground="#cfcfcf", font=("Consolas", 10))
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#e0a800")
        self.style.configure("Status.TLabel", font=("Segoe UI", 12))

        self.missing_libs = []
        self.missing_files = []

        self.create_widgets()
        self.run_diagnostics()

    def create_widgets(self):
        # Header
        header = ttk.Label(self, text="SYSTEM DIAGNOSTICS", style="Header.TLabel")
        header.pack(pady=20)

        # Status Frame
        self.status_frame = tk.Frame(self, bg="#1e1e1e")
        self.status_frame.pack(fill="x", padx=40)

        # Categories
        self.lbl_lib_status = self.create_status_row("Libraries")
        self.lbl_struct_status = self.create_status_row("Folder Structure")
        self.lbl_asset_status = self.create_status_row("Assets")

        # Log Area
        tk.Label(self, text="Diagnostic Log:", bg="#1e1e1e", fg="#888", anchor="w").pack(fill="x", padx=40,
                                                                                         pady=(20, 0))
        self.log_area = tk.Text(self, height=12, bg="#2b2b2b", fg="#00ff00", font=("Consolas", 9), bd=0, padx=10,
                                pady=10)
        self.log_area.pack(fill="both", expand=True, padx=40, pady=5)
        self.log_area.config(state=tk.DISABLED)

        # Action Button Area
        self.btn_action = tk.Button(
            self,
            text="SCANNING...",
            bg="#444",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            state=tk.DISABLED,
            command=self.handle_action
        )
        self.btn_action.pack(pady=20, ipadx=20, ipady=5)

    def create_status_row(self, text):
        frame = tk.Frame(self.status_frame, bg="#1e1e1e")
        frame.pack(fill="x", pady=5)

        lbl_name = tk.Label(frame, text=f"{text}:", width=25, anchor="w", bg="#1e1e1e", fg="#cfcfcf",
                            font=("Segoe UI", 10))
        lbl_name.pack(side="left")

        lbl_status = tk.Label(frame, text="WAITING", width=15, anchor="w", bg="#1e1e1e", fg="#888",
                              font=("Segoe UI", 10, "bold"))
        lbl_status.pack(side="left")

        return lbl_status

    def log(self, msg, color="#00ff00"):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.tag_config(color, foreground=color)
        self.log_area.insert(tk.END, f"> {msg}\n", color)
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    def set_status(self, label, status, color):
        label.config(text=status, fg=color)

    def run_diagnostics(self):
        self.log("Starting full system scan...", "white")
        threading.Thread(target=self._scan_process, daemon=True).start()

    def _scan_process(self):
        # 1. Check Libraries
        self.missing_libs = []
        for lib in REQUIRED_LIBS:
            if importlib.util.find_spec(lib) is None:
                if lib == "PIL":
                    if importlib.util.find_spec("Pillow") is None:
                        self.missing_libs.append("Pillow")
                else:
                    self.missing_libs.append(lib)

        if self.missing_libs:
            self.set_status(self.lbl_lib_status, "MISSING", "#ff4444")
            self.log(f"CRITICAL: Missing libraries: {', '.join(self.missing_libs)}", "#ff4444")
        else:
            self.set_status(self.lbl_lib_status, "OK", "#00ff00")
            self.log("Libraries checked. OK.")

        # 2. Check File Structure
        self.missing_files = []
        structure_errors = False

        for folder, files in FILE_STRUCTURE.items():
            # Check if folder exists (skip check for root '.')
            folder_path = folder if folder != "." else ""
            if folder != "." and not os.path.exists(folder_path):
                self.log(f"MISSING FOLDER: '{folder}/'", "#ff4444")
                structure_errors = True
                continue

            # Check files inside that folder
            for file in files:
                target_path = os.path.join(folder_path, file)
                if not os.path.exists(target_path):
                    self.missing_files.append(target_path)
                    self.log(f"MISSING FILE: {target_path}", "#ff4444")

        if self.missing_files or structure_errors:
            self.set_status(self.lbl_struct_status, "BROKEN", "#ff4444")
            self.log("Action: Please create folders 'gui' and 'backend' and move files.", "yellow")
        else:
            self.set_status(self.lbl_struct_status, "OK", "#00ff00")
            self.log("File structure checked. OK.")

        # 3. Check Assets
        missing_assets = []
        asset_dir = "assets"

        if not os.path.isdir(asset_dir):
            self.log("CRITICAL: 'assets' folder not found!", "#ff4444")
            missing_assets = REQUIRED_ASSETS
        else:
            for asset in REQUIRED_ASSETS:
                target = os.path.join(asset_dir, asset)
                if not os.path.exists(target):
                    missing_assets.append(asset)

        if missing_assets:
            self.set_status(self.lbl_asset_status, "INCOMPLETE", "#ff4444")
            self.log(f"Missing assets: {len(missing_assets)} file(s)", "#ff4444")
        else:
            self.set_status(self.lbl_asset_status, "OK", "#00ff00")
            self.log("Assets checked. OK.")

        # Final Decision
        is_structure_ok = not self.missing_files and not structure_errors and not missing_assets

        if self.missing_libs:
            self.btn_action.config(text="FIX DEPENDENCIES", bg="#e0a800", state=tk.NORMAL)
        elif not is_structure_ok:
            self.btn_action.config(text="STRUCTURE ERROR", bg="#ff4444", state=tk.DISABLED)
            self.log("Cannot fix structure automatically. Move files manually.", "white")
        else:
            self.btn_action.config(text="LAUNCH APP", bg="#00aa00", state=tk.NORMAL)
            self.log("System healthy. Ready to launch.", "#00ff00")

    def handle_action(self):
        text = self.btn_action.cget("text")
        if text == "FIX DEPENDENCIES":
            self.fix_dependencies()
        elif text == "LAUNCH APP":
            self.launch_app()

    def fix_dependencies(self):
        self.btn_action.config(state=tk.DISABLED)
        self.log("Installing libraries...", "yellow")

        def run_pip():
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", *self.missing_libs])
                self.log("Success! Re-scanning...", "#00ff00")
                self.after(1000, self.run_diagnostics)
            except subprocess.CalledProcessError as e:
                self.log(f"Error: {e}", "#ff4444")
                self.btn_action.config(state=tk.NORMAL)

        threading.Thread(target=run_pip, daemon=True).start()

    def launch_app(self):
        self.log("Launching main.py...", "#00ff00")
        self.destroy()
        subprocess.Popen([sys.executable, "main.py"])


if __name__ == "__main__":
    app = CoffeeTroubleshooter()
    app.mainloop()
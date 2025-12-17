import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import os
import sys
import importlib.util
import subprocess
import threading


class CoffeeTroubleshooter:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Machine Troubleshooter")
        self.root.geometry("600x500")
        self.root.configure(bg="#2b2b2b")

        # --- CONFIGURATION ---
        self.project_root = os.path.dirname(os.path.abspath(__file__))

        # Define what SHOULD be there based on your screenshots
        self.expected_structure = {
            "assets": [
                "logo.ico", "logo.png", "StartScreen.png", "OrderWindow.png",
                "EspressoWindow.png", "LatteWindow.png", "CappuccinoWindow.png",
                "PaymentWindow.png", "ChangeWindow.png"
                # Note: Add others if missing from this list
            ],
            "backend": ["__init__.py", "logic.py"],
            "gui": [
                "__init__.py", "gui_code.py", "employee_verification.py",
                "passcode_editor.py"
            ],
            ".": ["main.py", "requirements.txt", "employee_passcode.txt", "dependency_installer.py"]  # Root files
        }

        self.required_modules = ["ttkbootstrap", "PIL", "pygame", "gtts"]

        # --- UI LAYOUT ---

        # Header
        lbl_title = tk.Label(root, text="System Diagnostic Tool", font=("Segoe UI", 14, "bold"), bg="#2b2b2b",
                             fg="#e69138")
        lbl_title.pack(pady=10)

        # Button Frame
        btn_frame = tk.Frame(root, bg="#2b2b2b")
        btn_frame.pack(pady=5)

        self.btn_scan = tk.Button(btn_frame, text="1. Scan Files & Libs", bg="#2196F3", fg="white", width=20,
                                  command=self.run_full_scan)
        self.btn_scan.pack(side=tk.LEFT, padx=10)

        self.btn_test = tk.Button(btn_frame, text="2. Test Run (Catch Errors)", bg="#e91e63", fg="white", width=25,
                                  command=self.test_launch_app)
        self.btn_test.pack(side=tk.LEFT, padx=10)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(root, width=70, height=20, bg="#1e1e1e", fg="#00ff00",
                                                  font=("Consolas", 9))
        self.log_area.pack(pady=10, padx=10)
        self.log_area.insert(tk.END, "Waiting to scan...\n")
        self.log_area.config(state='disabled')

    def log(self, message, color="#00ff00"):
        self.log_area.config(state='normal')

        # Configure tag for color if not exists
        if color not in self.log_area.tag_names():
            self.log_area.tag_config(color, foreground=color)

        self.log_area.insert(tk.END, message + "\n", color)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def run_full_scan(self):
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')

        self.log("--- STARTING SYSTEM SCAN ---", "#ffffff")

        # 1. Check Files
        missing_files = []
        for folder, files in self.expected_structure.items():
            for file in files:
                if folder == ".":
                    path = os.path.join(self.project_root, file)
                else:
                    path = os.path.join(self.project_root, folder, file)

                if os.path.exists(path):
                    self.log(f"[OK] Found {folder}/{file}")
                else:
                    self.log(f"[MISSING] {folder}/{file}", "#ff0000")
                    missing_files.append(f"{folder}/{file}")

        # 2. Check Python Modules
        missing_libs = []
        for lib in self.required_modules:
            # Handle naming differences (PIL is imported as PIL, but installed as pillow)
            import_name = "PIL" if lib == "PIL" else lib
            spec = importlib.util.find_spec(import_name)
            if spec is not None:
                self.log(f"[OK] Library '{lib}' installed.")
            else:
                self.log(f"[MISSING] Library '{lib}' NOT found!", "#ff0000")
                missing_libs.append(lib)

        self.log("-" * 30, "#ffffff")

        if not missing_files and not missing_libs:
            self.log("Scan Complete: SYSTEM HEALTHY ✅", "#00ff00")
        else:
            self.log("Scan Complete: ISSUES FOUND ❌", "#ff0000")
            if missing_libs:
                self.log("TIP: Run 'dependency_installer.py' to fix libraries.", "#e69138")
            if missing_files:
                self.log("TIP: Check if files were moved or deleted.", "#e69138")

    def test_launch_app(self):
        self.log("\n--- ATTEMPTING TEST LAUNCH ---", "#ffffff")
        self.log("Running main.py and capturing output...", "#ffffff")

        target = os.path.join(self.project_root, "main.py")
        if not os.path.exists(target):
            self.log("Cannot test: main.py is missing!", "#ff0000")
            return

        # Run in a thread so GUI doesn't freeze
        threading.Thread(target=self._run_subprocess, args=(target,), daemon=True).start()

    def _run_subprocess(self, target):
        try:
            # We run python as a subprocess and pipe the output
            process = subprocess.Popen(
                [sys.executable, target],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate()

            if stdout:
                self.log(f"STDOUT: {stdout}", "#cccccc")

            if stderr:
                self.log("CRASH DETECTED (STDERR):", "#ff0000")
                self.log(stderr, "#ff4444")
                self.log("Analyze the error above to fix the crash.", "#e69138")
            elif process.returncode == 0:
                self.log("App closed successfully (No crash detected).", "#00ff00")
            else:
                self.log(f"App exited with code {process.returncode} but no error message?", "#ff0000")

        except Exception as e:
            self.log(f"Failed to launch subprocess: {e}", "#ff0000")


if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeTroubleshooter(root)
    root.mainloop()

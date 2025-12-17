import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import StringVar, Toplevel
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from backend import speak

current_script_path = os.path.abspath(__file__)
gui_folder_path = os.path.dirname(current_script_path)
project_root = os.path.dirname(gui_folder_path)

# --- Employ Passcode Screen ---
class EmployeeCodeDialog(Toplevel):
    def __init__(self, master, title="Employee Access", callback=None):
        super().__init__(master)
        self.master = master
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.passcode_path = os.path.join(project_root, "employee_passcode.txt")
        with open(self.passcode_path) as pass_: self.passcode=pass_.read()
        self.result = False
        self.callback=callback

        # Make this window modal
        self.transient(master)
        self.grab_set()
        self.focus_set()

        self.var = StringVar()

        # Label
        lbl = ttk.Label(self, text="Enter Employee Passcode:", font=("Segoe UI", 10))
        lbl.pack(pady=(20, 5))

        # Entry
        self.entry = ttk.Entry(self, textvariable=self.var, show="*", width=20)
        self.entry.pack(pady=5)
        self.entry.focus_set()

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(10, 10))

        btn_ok = ttk.Button(btn_frame, text="OK", bootstyle=SUCCESS, command=self.check_code)
        btn_ok.pack(side=LEFT, padx=5)

        btn_cancel = ttk.Button(btn_frame, text="Cancel", bootstyle=DANGER, command=self.destroy)
        btn_cancel.pack(side=LEFT, padx=5)

        # Bind Enter key
        self.entry.bind("<Return>", lambda e: self.check_code())
        self.entry.bind("<Escape>", lambda e: self.destroy())

    def check_code(self):
        if self.var.get() == self.passcode:
            self.master.employee_mode=True
            speak("Employee mode enabled.")
            callback=self.callback
            if callback:
                callback()
            self.destroy()
        else:
            # Wrong code feedback
            self.var.set("")
            self.entry.focus_set()
            self.geometry("300x200")
            self.error_label = ttk.Label(self, text="", foreground="red")
            self.error_label.pack(side=BOTTOM, pady=10)
            self.error_label.config(text="Incorrect passcode!")
            speak("Incorrect passcode!")

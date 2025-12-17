import ttkbootstrap as ttk
from ttkbootstrap import Toplevel, StringVar
from ttkbootstrap.constants import *
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from backend import speak

current_script_path = os.path.abspath(__file__)
gui_folder_path = os.path.dirname(current_script_path)
project_root = os.path.dirname(gui_folder_path)

class PasscodeEditor(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Passcode Editor")
        self.geometry("300x150")
        self.passcode_path = os.path.join(project_root, "employee_passcode.txt")
        with open(self.passcode_path) as pass_: self.passcode = pass_.read()

        self.transient(master)
        self.grab_set()
        self.focus_set()

        self.var = StringVar()

        # Label
        self.lbl = ttk.Label(self, text="Enter Current Employee Code:", font=("Segoe UI", 10))
        self.lbl.pack(pady=(20, 5))
        self.error_label = ttk.Label(self, text="", foreground="red")

        # Entry
        self.entry = ttk.Entry(self, textvariable=self.var, show="*", width=20)
        self.entry.pack(pady=5)
        self.entry.focus_set()

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=(10, 10))

        self.btn_ok = ttk.Button(btn_frame, text="OK", bootstyle=SUCCESS, command=self.check_code)
        self.btn_ok.pack(side=LEFT, padx=5)

        self.btn_cancel = ttk.Button(btn_frame, text="Cancel", bootstyle=DANGER, command=self.destroy)
        self.btn_cancel.pack(side=LEFT, padx=5)

        # Bind Enter key
        self.entry.bind("<Return>", lambda e: self.check_code())
        self.entry.bind("<Escape>", lambda e: self.destroy())

    def check_code(self):
        if self.var.get() == self.passcode.replace(" ", ""):
            speak("Enter new employee code!")
            self.lbl.config(text="Enter new passcode:")
            self.entry.delete(0, "end")
            self.entry.bind("<Return>", lambda e: self.save_code())
            self.btn_ok.config(command=self.save_code)
        else:
            # Wrong code feedback
            self.var.set("")
            self.entry.focus_set()
            self.geometry("300x200")
            self.error_label.pack(side=BOTTOM, pady=10)
            self.error_label.config(text="Incorrect passcode!")
            speak("Incorrect passcode!")

    def save_code(self):
        self.geometry("300x150")
        self.error_label.config(text="")
        new_code = self.entry.get()
        if new_code and " " in new_code:
            self.error_label.pack(side=BOTTOM, pady=10)
            self.error_label.config(text="Please enter a valid new passcode.")
            speak("Please enter a valid new passcode.")
        elif new_code:
            with open(self.passcode_path, "w") as pass_:
                pass_.write(new_code)
            speak("Passcode saved!")
            self.passcode = new_code
            self.destroy()
        else:
            self.error_label.pack(side=BOTTOM, pady=10)
            self.error_label.config(text="Please enter a valid new passcode.")
            speak("Please enter a valid new passcode.")

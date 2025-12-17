import ttkbootstrap as ttk
from ttkbootstrap import Button, Toplevel, StringVar
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os, sys, webbrowser

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from backend import verify_resources, machine, process_payment, speak
from .employee_verification import EmployeeCodeDialog
from .passcode_editor import PasscodeEditor

current_script_path = os.path.abspath(__file__)
gui_folder_path = os.path.dirname(current_script_path)
project_root = os.path.dirname(gui_folder_path)


# --- CONTROLLER CLASS (THE TV FRAME) ---
class CoffeeApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Coffee Machine")
        self.geometry("540x960")
        self.resizable(True, True)

        self.drink=""
        self.employee_mode=False

        # Set icon ONCE for the whole app
        icon_path = os.path.join(project_root, "assets", "logo.ico")
        self.iconbitmap(icon_path)

        # Show the first screen
        self.show_start_screen()

        self.mainloop()

    def clear_screen(self):
        # Destroy current content before showing new content
        for widget in self.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_screen()
        # Create the Start Frame and pack it
        start_page = StartPage(self)
        start_page.pack(fill="both", expand=True)

    def show_order_screen(self):
        self.clear_screen()
        order_page = OrderPage(self)
        order_page.pack(fill="both", expand=True)

    def show_payment_screen(self, cost):
        self.clear_screen()
        # We pass the 'cost' to the payment page
        payment_page = PaymentPage(self, cost)
        payment_page.pack(fill="both", expand=True)

    def show_give_change_screen(self, change):
        self.clear_screen()
        # Pass the change amount to the page
        payment_page = GiveChangePage(self, change)
        payment_page.pack(fill="both", expand=True)

    def show_delivery_screen(self):
        self.clear_screen()
        # FIX: Use GiveDrinkPage, not PaymentPage
        delivery_page = GiveDrinkPage(self)
        delivery_page.pack(fill="both", expand=True)

    def manage_employee_mode(self):
        if self.employee_mode:
            self.employee_mode=False
            speak("Employee mode disabled.")
        else:
            EmployeeCodeDialog(self)

    def refill_machine(self):
        if self.employee_mode:
            machine.refill()
            speak("Machine refilled.")
        else:
            EmployeeCodeDialog(self, callback=self.refill_machine)
            speak("Please call an employee to refill the machine!")

#--- Basic SCREEN class ---
class Screen(ttk.Frame):
    def __init__(self, master, screen):
        super().__init__(master)
        self.focus_set()

        self.master = master

        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Logic to load image
        screen3_path = os.path.join(project_root, "assets", screen)
        pil_image = Image.open(screen3_path)
        pil_image = pil_image.resize((540, 960), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)

        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        self.bind("<e>", lambda e: self.master.manage_employee_mode())
        self.bind("<r>", lambda e: self.master.refill_machine())

        self.mail = self.canvas.create_text(
            187, 840,
            text="akshajgoel@bnpsramvihar.edu.in",
            fill="#FFF3DC",
            font=("Segoe UI", 8)
        )

        self.web_link = self.canvas.create_text(
            430, 840,
            text="aksweb.me",
            fill="#FFF3DC",
            font=("Segoe UI", 8)
        )

        def mail(event):
            webbrowser.open_new("mailto:akshajgoel@bnpsramvihar.edu.in")

        def open_link(event):
            webbrowser.open_new("https://aksweb.me")

        self.canvas.tag_bind(self.mail, "<Button-1>", mail)
        self.canvas.tag_bind(self.mail, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.mail, "<Leave>", lambda e: self.canvas.config(cursor=""))

        self.canvas.tag_bind(self.web_link, "<Button-1>", open_link)
        self.canvas.tag_bind(self.web_link, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind(self.web_link, "<Leave>", lambda e: self.canvas.config(cursor=""))


# --- SCREEN 1: START (Converted to Frame) ---
class StartPage(Screen):
    def __init__(self, master):
        super().__init__(master, "StartScreen.png")

        speak("Welcome, to the A.K.S Cafe")

        btn_order = Button(
            self,
            text="Order a Coffee",
            bootstyle="warning",
            width=30,
            command=self.master.show_order_screen  # Call controller function
        )
        btn_order.place(x=140, y=550)
        self.canvas.create_window(270, 550, window=btn_order)

        btn_exit = Button(
            self,
            text="Exit",
            bootstyle="warning",
            width=30,
            command=self.master.destroy
        )
        self.canvas.create_window(270, 600, window=btn_exit)

        self.btn_passcode_change = Button(
            self,
            text="Change Employee Passcode",
            bootstyle="warning",
            width=30,
            command=lambda e: PasscodeEditor(self.master)
        )

        self.bind("<e>", lambda e: self.custom_employee_manage())
        self.bind("<p>", lambda e: PasscodeEditor(self.master))

    def custom_employee_manage(self):
        if self.master.employee_mode:
            self.master.employee_mode=False
            speak("Employee mode disabled.")
        else:
            EmployeeCodeDialog(self.master, callback=self.passcode_editor)

    def passcode_editor(self):
        if self.master.employee_mode:
            self.canvas.create_window(270, 650, window=self.btn_passcode_change)
        else:
            if self.btn_passcode_change.winfo_exists():
                self.btn_passcode_change.destroy()


# --- SCREEN 2: ORDER (Converted to Frame) ---
class OrderPage(Screen):
    def __init__(self, master):
        super().__init__(master, "OrderWindow.png")

        speak("Which coffee would you like?")

        # Buttons
        btn_espresso = Button(self, text="Espresso ($1.50)", bootstyle="warning", width=20,
                              command=lambda: self.select_drink("espresso"))
        self.canvas.create_window(270, 550, window=btn_espresso)

        btn_latte = Button(self, text="Latte ($2.50)", bootstyle="warning", width=20,
                           command=lambda: self.select_drink("latte"))
        self.canvas.create_window(270, 600, window=btn_latte)

        btn_cappuccino = Button(self, text="Cappuccino ($3.00)", bootstyle="warning", width=20,
                                command=lambda: self.select_drink("cappuccino"))
        self.canvas.create_window(270, 650, window=btn_cappuccino)

    def select_drink(self, drink_name):
        is_enough, missing_item = verify_resources(drink_name)

        if is_enough:
            # Look up cost from backend machine data
            cost = machine.MENU[drink_name]["cost"]
            self.master.drink=drink_name.title()
            # Tell controller to switch screens
            self.master.show_payment_screen(cost)
        else:
            speak(f"Sorry! Not enough {missing_item} in the machine.")


# --- SCREEN 3: PAYMENT (Converted to Frame) ---
class PaymentPage(Screen):
    def __init__(self, master, cost):
        super().__init__(master, "PaymentWindow.png")
        self.cost = cost

        speak(f"Please pay ${cost}")

        self.canvas.create_text(
            270, 420,
            text=f"Please insert ${self.cost}",
            fill="#6D1F00",
            font=("Segoe UI", 16, "bold")
        )

        # Spinboxes
        self.pennies = ttk.Spinbox(self, from_=0, to=300, width=5, bootstyle="warning")
        self.nickels = ttk.Spinbox(self, from_=0, to=60, width=5, bootstyle="warning")
        self.dimes = ttk.Spinbox(self, from_=0, to=30, width=5, bootstyle="warning")
        self.quarters = ttk.Spinbox(self, from_=0, to=12, width=5, bootstyle="warning")
        self.dollars = ttk.Spinbox(self, from_=0, to=3, width=5, bootstyle="warning")

        coins = [("Pennies", self.pennies), ("Nickels", self.nickels), ("Dimes", self.dimes),
                 ("Quarters", self.quarters), ("Dollars", self.dollars)]

        self.pennies_val=0
        self.nickels_val=0
        self.dimes_val=0
        self.quarters_val=0
        self.dollars_val=0
        self.coins_val = [(self.pennies_val, self.pennies), (self.nickels_val, self.nickels), (self.dimes_val, self.dimes),
                 (self.quarters_val, self.quarters), (self.dollars_val, self.dollars)]

        x_pos = 80
        for name, spinbox in coins:
            self.canvas.create_text(
                x_pos, 470,
                text=name,
                fill="#6D1F00",
            )
            self.canvas.create_window(x_pos, 500, window=spinbox)
            x_pos += 90

        btn_pay = Button(self, text="Insert Money", bootstyle="warning", width=20,
                         command=lambda: self.pay())
        self.canvas.create_window(270, 600, window=btn_pay)


    def pay(self):
        is_enough, change, payment = process_payment(
            self.cost,
            self.pennies.get(),
            self.nickels.get(),
            self.dimes.get(),
            self.quarters.get(),
            self.dollars.get()
        )
        if not payment:
            speak("Sorry! The machine doesn't have enough money, please enter a lower amount.")
        elif is_enough and payment:
            if change == 0:
                self.master.show_delivery_screen()
            else:
                # We need to pass 'change' to this screen so we can display it!
                self.master.show_give_change_screen(change)
        else:
            speak(f"Not enough money! Please insert ${self.cost-payment} more.")


class GiveChangePage(Screen):
    def __init__(self, master, change):
        super().__init__(master, "ChangeWindow.png")
        # Show the Change Amount
        self.canvas.create_text(
            270, 450,
            text=f"Here is your change:\n${change}",
            fill="#6D1F00",
            font=("Segoe UI", 20, "bold"),
            justify="center"
        )

        speak(f"Here is your change of ${change}.")

        # Button to collect change and move to delivery
        btn_collect = Button(
            self,
            text="Collect Change",
            bootstyle="warning",
            width=20,
            command=self.master.show_delivery_screen
        )
        self.canvas.create_window(270, 600, window=btn_collect)


class GiveDrinkPage(Screen):
    def __init__(self, master):
        super().__init__(master, "DeliveryWindow.png")

        self.canvas.create_text(
            280, 370,
            text="Enjoy your Coffee! ☕",
            fill="#6D1F00",
            font=("Segoe UI", 24, "bold")
        )
        speak(f"Enjoy your {self.master.drink}. Thank you for choosing us.")

        # Button to restart
        btn_home = Button(
            self,
            text="Order Again",
            bootstyle="warning",
            width=20,
            command=self.master.show_order_screen
        )
        self.canvas.create_window(270, 770, window=btn_home)

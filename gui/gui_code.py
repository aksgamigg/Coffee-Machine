import ttkbootstrap as ttk
from ttkbootstrap import Label, Button
from PIL import Image, ImageTk
import os, sys, webbrowser
# 1. Get the directory where gui.py lives
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Go up one level to the project root ('CoffeeMachine' folder)
parent_dir = os.path.dirname(current_dir)

# 3. Add that root directory to python's search path
sys.path.append(parent_dir)
from backend import verify_resources, machine, process_payment

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


# --- SCREEN 1: START (Converted to Frame) ---
class StartPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master  # Save reference to the App controller

        # Logic to load image
        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        screen3_path = os.path.join(project_root, "assets", "StartScreen.png")
        pil_image = Image.open(screen3_path)
        pil_image = pil_image.resize((540, 960), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)

        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

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


# --- SCREEN 2: ORDER (Converted to Frame) ---
class OrderPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.drink = None

        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        screen3_path = os.path.join(project_root, "assets", "OrderWindow.png")
        pil_image = Image.open(screen3_path)
        pil_image = pil_image.resize((540, 960), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)

        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

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

    def select_drink(self, drink_name):
        is_enough, missing_item = verify_resources(drink_name)

        if is_enough:
            # Look up cost from backend machine data
            cost = machine.MENU[drink_name]["cost"]
            self.drink = drink_name.title()
            self.master.drink=self.drink
            # Tell controller to switch screens
            self.master.show_payment_screen(cost)
        else:
            error_text = f"Sorry! Not enough {missing_item}."
            lbl_error = Label(self, text=error_text, bootstyle="danger", font=("Segoe UI", 12, "bold"))
            lbl_error.pack(side="bottom", pady=20)


# --- SCREEN 3: PAYMENT (Converted to Frame) ---
class PaymentPage(ttk.Frame):
    def __init__(self, master, cost):
        super().__init__(master)
        self.master = master
        self.cost = cost

        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        screen3_path = os.path.join(project_root, "assets", "PaymentWindow.png")
        pil_image = Image.open(screen3_path)
        pil_image = pil_image.resize((540, 960), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)

        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        self.canvas.create_text(
            270, 420,
            text=f"Please insert ${self.cost}",
            fill="#6D1F00",
            font=("Segoe UI", 16, "bold")
        )

        # Spinboxes
        self.pennies = ttk.Spinbox(self, from_=0, to=100, width=5, bootstyle="warning")
        self.nickels = ttk.Spinbox(self, from_=0, to=100, width=5, bootstyle="warning")
        self.dimes = ttk.Spinbox(self, from_=0, to=100, width=5, bootstyle="warning")
        self.quarters = ttk.Spinbox(self, from_=0, to=100, width=5, bootstyle="warning")
        self.dollars = ttk.Spinbox(self, from_=0, to=100, width=5, bootstyle="warning")

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

    def pay(self):
        # 1. Get values directly from the Spinboxes
        # We use 'or 0' to handle cases where the box might be empty
        try:
            pennies = int(self.pennies.get() or 0)
            nickels = int(self.nickels.get() or 0)
            dimes = int(self.dimes.get() or 0)
            quarters = int(self.quarters.get() or 0)
            dollars = int(self.dollars.get() or 0)
        except ValueError:
            # Safety net if they type text instead of numbers
            pennies = nickels = dimes = quarters = dollars = 0

        # 2. Pass these new values to the backend
        is_enough, change = process_payment(
            self.cost,
            pennies,
            nickels,
            dimes,
            quarters,
            dollars
        )

        if is_enough:
            if change == 0:
                self.master.show_delivery_screen()
            else:
                # We need to pass 'change' to this screen so we can display it!
                self.master.show_give_change_screen(change)
        else:
            self.canvas.create_text(
                270, 700,
                text=f"Not enough money! Need ${self.cost}",
                fill="red",
                font=("Segoe UI", 12, "bold")
            )


class GiveChangePage(ttk.Frame):
    def __init__(self, master, change):
        super().__init__(master)
        self.master = master

        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # Load your ChangeWindow.png here
        screen_path = os.path.join(project_root, "assets", "ChangeWindow.png")
        pil_image = Image.open(screen_path)
        pil_image = pil_image.resize((540, 960), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        # Show the Change Amount
        self.canvas.create_text(
            270, 450,
            text=f"Here is your change:\n${change}",
            fill="#6D1F00",
            font=("Segoe UI", 20, "bold"),
            justify="center"
        )

        # Button to collect change and move to delivery
        btn_collect = Button(
            self,
            text="Collect Change",
            bootstyle="warning",
            width=20,
            command=self.master.show_delivery_screen
        )
        self.canvas.create_window(270, 600, window=btn_collect)

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


class GiveDrinkPage(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.canvas = ttk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)

        # You might want specific images for specific drinks later,
        # but for now, let's use a generic delivery image (or one of your windows)
        # Assuming you have a 'CappuccinoWindow.png' or similar you want to show final result on.
        # For now, I'll reuse StartScreen just to test, but you should swap this!
        screen_path = os.path.join(project_root, "assets", f"{self.master.drink}Window.png")
        pil_image = Image.open(screen_path)
        pil_image = pil_image.resize((540, 960), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(pil_image)
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")

        self.canvas.create_text(
            280, 370,
            text="Enjoy your Coffee! ☕",
            fill="#6D1F00",
            font=("Segoe UI", 24, "bold")
        )

        # Button to restart
        btn_home = Button(
            self,
            text="Order Again",
            bootstyle="warning",
            width=20,
            command=self.master.show_order_screen
        )
        self.canvas.create_window(270, 770, window=btn_home)

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
# ☕ CoffeeMachine `v0.1.0-alpha`

> A fully-featured Python desktop vending machine simulator. Order espresso, latte, or cappuccino, manage resources, handle payments with coins/bills—all with a sleek dark-themed GUI.
>
> ⚠️ **Alpha Status**: This project is still in active development. Features may change, and not everything is complete yet.

![Status Badge](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange) ![Version](https://img.shields.io/badge/Version-0.1.0--alpha-yellow)

---

## 🎯 What This Does

CoffeeMachine is an interactive vending machine application built with Python. It simulates a real coffee machine with:

- **3 drink options**: Espresso, Latte, Cappuccino (with different recipes and prices)
- **Resource management**: Tracks water, milk, and coffee levels dynamically
- **Coin/bill payment system**: Processes coins (pennies, nickels, dimes, quarters) + dollar bills with change calculation
- **Smart diagnostics**: Automated system checks for dependencies, file structure, and assets
- **Refill & reset features**: Keep the machine running smoothly

Perfect for learning GUI development, object-oriented design, or just having fun with a desktop app!

---

## 📁 Project Structure

```
CoffeeMachine/
├── main.py                      # Entry point (launches the app)
├── dependency_installer.py      # One-click dependency setup
├── troubleshooter.py            # System diagnostics & health checks
├── requirements.txt             # Python dependencies
│
├── gui/
│   └── gui_code.py             # All Tkinter UI screens & components
│
├── backend/
│   └── logic.py                # Core business logic (CoffeeMachine class)
│
└── assets/
    ├── logo.ico                # App icon
    ├── logo.png                # Logo image
    ├── StartScreen.png         # Welcome screen background
    ├── OrderWindow.png         # Order menu UI
    ├── PaymentWindow.png       # Payment screen UI
    ├── ChangeWindow.png        # Change return screen UI
    ├── EspressoWindow.png      # Espresso brewing UI
    ├── LatteWindow.png         # Latte brewing UI
    └── CappuccinoWindow.png    # Cappuccino brewing UI
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** installed
- Git (optional, for cloning)

### Installation

**Option 1: Automatic Setup (Recommended)**
```bash
python dependency_installer.py
```
This launches a GUI that installs all dependencies and starts the app. No terminal needed.

**Option 2: Manual Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### First Time Running?
If something's wrong, the **system will catch it**:
```bash
python troubleshooter.py
```
This runs full diagnostics (checks libraries, file structure, assets) and can auto-fix missing dependencies.

---

## 💻 How to Use

1. **Start the app**: `python main.py`
2. **Select a drink**: Click Espresso ($1.50), Latte ($2.50), or Cappuccino ($3.00)
3. **Pay**: Enter coins and bills
4. **Get change**: Machine calculates and returns your change
5. **Repeat**: The machine refills automatically when it runs out of resources

---

## 🔧 Technical Details

### Dependencies
| Package | Purpose |
|---------|---------|
| `ttkbootstrap` | Modern-looking Tkinter themes |
| `Pillow` | Image handling for UI backgrounds |

### Core Classes

#### `CoffeeMachine` (backend/logic.py)
Main business logic:
```python
machine = CoffeeMachine()
is_valid, missing_item = verify_resources("espresso")
is_paid, change = process_payment(total_cost, pennies, nickels, dimes, quarters, dollars)
```

**Key features:**
- Resource tracking (water, milk, coffee)
- Menu definitions (recipes + prices)
- Payment validation with floating-point safety

#### `DependencyInstaller` (dependency_installer.py)
GUI-based setup wizard:
- One-click pip install for dependencies
- Progress tracking
- Auto-launches main app after install

#### `CoffeeTroubleshooter` (troubleshooter.py)
Automated health checks:
- Scans for required libraries
- Verifies folder structure
- Checks for missing assets
- Can auto-fix dependency issues

### GUI Architecture
The GUI uses **Tkinter** with:
- Dark theme styling (custom colors + ttkbootstrap)
- Image-based window designs (PNG backgrounds)
- Separate screens: StartScreen → OrderWindow → PaymentWindow → [Drink]Window → ChangeWindow

---

## 🎓 Learning Points

This project demonstrates:

✅ **Object-Oriented Design** – Clean CoffeeMachine class with state management  
✅ **GUI Development** – Tkinter layouts, event handling, window management  
✅ **Error Handling** – Resource checks, payment validation, floating-point precision  
✅ **Project Structure** – Backend/frontend separation, clean dependencies  
✅ **Automation** – Dependency installation & system diagnostics  
✅ **User Experience** – Responsive UI, clear status messages, helpful error logs  

---

## 🛠️ Customization

### Change Coffee Prices
Edit `backend/logic.py`:
```python
self.MENU = {
    "espresso": {"ingredients": {...}, "cost": 1.50},  # Change 1.50
    "latte": {"ingredients": {...}, "cost": 2.50},     # Change 2.50
    # ...
}
```

### Add a New Drink
1. Add recipe to `MENU` in `logic.py`
2. Create corresponding UI window in `gui/gui_code.py`
3. Add drink preview image to `assets/`

### Tweak Resources
Edit the starting amounts in `CoffeeMachine.__init__()`:
```python
self.resources = {
    "water": 300,    # Change this
    "milk": 200,     # Or this
    "coffee": 100,   # Or this
}
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'ttkbootstrap'"
→ Run: `python dependency_installer.py`

### Missing asset images
→ Run: `python troubleshooter.py` (will tell you exactly what's missing)

### Folder structure broken
→ Make sure your project layout matches the structure above. Folders must exist: `gui/`, `backend/`, `assets/`

### Floating-point payment errors
→ Already handled! The code rounds to 2 decimal places to prevent weird $0.0000000001 issues.

---

## 📊 Project Stats

- **Lines of Code**: ~1,500 (logic + GUI combined)
- **Time to Build**: Perfect for a weekend project
- **Skill Level**: Intermediate Python
- **Python Version**: 3.8+

---

## 🎉 Future Ideas

- 🎨 Add theme customization
- 📊 Transaction history/sales tracking
- 🔐 Admin panel (refill, pricing changes)
- 🌐 Network mode (multiple machines)
- 📱 Mobile companion app

---

## 📝 License

MIT License – Use it freely! Attribution appreciated but not required.

---

## 👨‍💻 Author

**Akshaj Goel**

- 🌐 **Website**: [aksweb.me](https://aksweb.me)
- 🐙 **GitHub**: [@aksgamigg](https://github.com/aksgamigg)

Built with ☕ by a developer learning Tkinter, OOP, and project architecture.

**Want to contribute?**
- Found a bug? File an issue
- Have an idea? Open a discussion
- Want to improve it? PRs welcome!

---

## 🤔 Questions?

Check `troubleshooter.py` for system diagnostics, or review the code comments in `logic.py` and `gui/gui_code.py`.

---

**Happy brewing! ☕**

# ☕ CoffeeMachine

> A fully-featured Python desktop vending machine simulator with realistic resource management, voice feedback, employee controls, and built-in diagnostics.

![Version](https://img.shields.io/badge/Version-0.2.0--alpha-orange?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=flat-square)

**Live Demo:** [aksweb.me/Coffee-Machine](https://aksweb.me/Coffee-Machine)  
**Portfolio:** [aksweb.me](https://aksweb.me)

---

## 🎯 Overview

CoffeeMachine is an interactive Python desktop application that simulates a real vending machine. Order espresso, latte, or cappuccino with realistic resource management, coin/bill payment processing, voice feedback via text-to-speech, and a full employee administration system.

Perfect for learning **OOP design**, **GUI development with Tkinter**, **state management**, **multi-threading**, and **security best practices**.

---

## ✨ Key Features

### 🎮 **Interactive GUI**
- Dark-themed interface built with **Tkinter** + **ttkbootstrap**
- Image-based screens (Start, Order, Payment, Delivery)
- Real beverage selection and payment flow
- Responsive button controls and status displays

### 💰 **Smart Payment System**
- Coin/bill input: pennies, nickels, dimes, quarters, dollars
- Floating-point safe calculations (no rounding errors)
- Automatic change calculation and return
- Payment validation before dispensing

### 📊 **Dynamic Resource Management**
- Track water, milk, and coffee levels in real-time
- Machine refuses orders if resources are insufficient
- Resource depletion warnings to users
- Accurate ingredient tracking per beverage

### 🎤 **Voice Feedback**
- Text-to-speech using **gTTS** (Google Translate API)
- **Pygame** for audio playback
- Machine "speaks" order confirmations, status updates, and errors
- Background threading for non-blocking audio

### 🔐 **Employee Mode**
- Passcode-protected admin access
- **Features:**
  - Refill machine supplies (water, milk, coffee, cash)
  - Change employee passcode securely
  - View machine diagnostics
  - Reset machine state
- Passcode stored in `employeepasscode.txt` (editable via GUI)
- Secure verification on each access

### 🔧 **Built-in Diagnostics**
- **troubleshooter.py** scans system for:
  - Missing asset files (images, icons)
  - Missing Python libraries
  - File structure validation
- Test-run capability with error capture
- Auto-detection of common issues

### 📦 **Dependency Installer**
- **dependency_installer.py** handles all setup
- Auto-detects Python environment
- Installs packages from `requirements.txt`
- Launches app after successful setup
- GUI progress indicator

### 🏗️ **Clean Architecture**
- **backend/logic.py** – Payment, resource, and beverage logic
- **gui/gui_code.py** – Screen management and UI components
- **gui/employee_verification.py** – Passcode verification
- **gui/passcode_editor.py** – Employee passcode management
- Separation of concerns for maintainability

---

## 📋 Requirements

**System Requirements:**
- Python 3.8 or higher
- Windows, macOS, or Linux
- ~100MB disk space for dependencies

**Python Packages:**
```
ttkbootstrap==1.6.11
Pillow>=9.0.0
pygame>=2.1.0
gTTS>=2.2.4
```

---

## 🚀 Installation & Setup

### Option 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/aksgamigg/CoffeeMachine.git
cd CoffeeMachine

# Run dependency installer
python dependency_installer.py
```

The installer will:
1. Check for Python 3.8+
2. Install all required packages
3. Launch the application automatically

### Option 2: Manual Setup

```bash
# Clone repository
git clone https://github.com/aksgamigg/CoffeeMachine.git
cd CoffeeMachine

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Option 3: Troubleshoot & Diagnose

If you encounter issues:

```bash
# Run the troubleshooter
python troubleshooter.py
```

The troubleshooter will:
- Scan for missing files and libraries
- Display diagnostic results in a GUI
- Suggest fixes for common errors
- Test-run the app and capture error output

---

## 🎮 How to Use

### Customer Mode

1. **Launch the app:** `python main.py`
2. **Select a beverage:**
   - Espresso: $1.50
   - Latte: $2.50
   - Cappuccino: $3.00
3. **Insert payment:** Use spinboxes to enter coins/bills
4. **Collect drink:** Machine dispenses beverage (voice prompt)
5. **Collect change:** Change is returned if overpaid

### Employee Mode

#### **Accessing Employee Controls**

Press **`E`** on the keyboard while the app is running to trigger employee mode:
- A passcode dialog will appear
- Default passcode: `1234` (stored in `employeepasscode.txt`)
- Enter correct passcode to enable admin access

#### **Employee Features**

Once logged in, employees can:

**1. Refill Supplies**
- Press **`R`** to refill machine
- Replenishes: water (300ml), milk (200ml), coffee (100g), cash ($20)
- Returns to customer home screen after refill

**2. Change Employee Passcode**
- Press **`P`** while in employee mode
- Dialog prompts for old and new passcode
- New passcode saved to `employeepasscode.txt`
- Changes take effect immediately on next access

**3. View Diagnostics**
- Machine automatically reports resource levels
- Status displayed via voice feedback
- Visual indicators on payment screen

**4. Reset Machine State**
- Refill clears all transactions
- Returns to initial operational state
- Useful after long downtime

---

## 📁 Project Structure

```
CoffeeMachine/
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── employeepasscode.txt             # Employee passcode (editable)
├── dependency_installer.py          # Automated setup wizard
├── troubleshooter.py                # Diagnostic tool
│
├── backend/
│   ├── __init__.py
│   ├── logic.py                     # Payment, resources, beverage logic
│   └── employee_verification.py     # Passcode verification logic
│
├── gui/
│   ├── __init__.py
│   ├── gui_code.py                  # Screen management, UI components
│   ├── employee_verification.py     # Employee login dialog
│   ├── passcode_editor.py           # Passcode editor GUI
│   └── employee_verification.py     # Employee mode logic
│
└── assets/
    ├── logo.ico                     # App icon
    ├── logo.png                     # Logo image
    ├── StartScreen.png              # Start screen background
    ├── OrderWindow.png              # Order selection screen
    ├── PaymentWindow.png            # Payment input screen
    ├── ChangeWindow.png             # Change return screen
    └── DeliveryWindow.png           # Delivery confirmation screen
```

---

## 🔐 Employee Mode Security

### Password Protection
- Passcode required for ALL admin actions
- Incorrect entries logged and prevented
- Passcode stored in plain text (intended for demo) — upgrade to hashing for production

### Passcode Management
- **Default:** `1234`
- **Change via GUI:** Press `P` in employee mode
- **Manual change:** Edit `employeepasscode.txt` directly
- Changes take effect immediately on next login

### Best Practices
- Change default passcode on first use
- Use strong, memorable passcode (4+ characters)
- Restrict physical access to machine
- Log all employee actions for audit trail (future enhancement)

---

## 🛠️ Technical Architecture

### Backend (`backend/logic.py`)
```python
class CoffeeMachine:
    - __init__()          # Initialize machine state
    - refill()            # Reset supplies
    - verify_resources()  # Check ingredient availability
    - process_payment()   # Handle coin/bill transactions
    - speak()             # Text-to-speech output
```

### GUI (`gui/gui_code.py`)
**Screen Flow:**
1. **StartPage** → "Welcome, order or exit?"
2. **OrderPage** → Select beverage (Espresso/Latte/Cappuccino)
3. **PaymentPage** → Insert coins/bills
4. **GiveChangePage** → Return change if overpaid
5. **GiveDrinkPage** → Dispense beverage, offer repeat order

### Employee Mode (`gui/employee_verification.py`)
```python
class EmployeeCodeDialog:
    - Prompt for passcode
    - Verify against employeepasscode.txt
    - Grant access to admin functions
    - Trigger refill or passcode editor
```

### Voice Feedback (`backend/logic.py` - `speak()`)
```python
def speak(text):
    - Generate MP3 via gTTS
    - Play using pygame.mixer
    - Run in background thread (daemon=True)
    - Non-blocking, doesn't freeze GUI
```

---

## 🐛 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| **"Module not found"** | Run `python dependency_installer.py` to install packages |
| **App won't start** | Run `python troubleshooter.py` to diagnose |
| **No sound output** | Check system volume, ensure pygame is installed |
| **Employee mode locked** | Passcode may be incorrect or `employeepasscode.txt` missing |
| **Missing images** | Ensure `assets/` folder exists with all PNG files |
| **Floating point errors** | Payment calculations use `round(x, 2)` — this is intentional |

### Running Diagnostics

```bash
python troubleshooter.py
```

Checks:
- ✅ Python version (3.8+)
- ✅ All required libraries installed
- ✅ Asset files present
- ✅ File structure intact
- ✅ Test-run app and capture errors

---

## 📚 Learning Outcomes

By studying and building on CoffeeMachine, you'll learn:

### **Core Python**
- Object-Oriented Design (OOP)
- State management
- Exception handling
- File I/O (storing passcodes, configs)

### **GUI Development**
- Tkinter widgets and layout
- ttkbootstrap theming
- Canvas and image rendering
- Event-driven architecture

### **Advanced Topics**
- Multi-threading (background voice playback)
- API integration (gTTS)
- Floating-point arithmetic safety
- Security (passcode verification)
- Dependency management

### **Software Engineering**
- Clean code architecture (backend/gui separation)
- Error handling and recovery
- User feedback and UX
- Automated testing (diagnostics)

---

## 🎯 Version History

**v0.2.0-alpha** (December 2025)
- Enhanced employee mode with diagnostics
- Improved troubleshooter with asset scanning
- Better error handling and recovery
- Multi-threading optimization for voice feedback

**v0.1.0-alpha** (December 2025)
- Initial release
- Core vending machine logic
- Payment system with coins/bills
- Voice feedback via gTTS + pygame
- Employee mode with passcode protection
- Dependency installer
- Built-in troubleshooter
- 3 beverage options (Espresso, Latte, Cappuccino)

---

## 🚀 Future Enhancements

- [ ] Database integration for transaction logging
- [ ] Advanced security (password hashing with bcrypt)
- [ ] Admin dashboard with sales analytics
- [ ] Multiple machine management
- [ ] Configuration file for customization
- [ ] Unit tests and integration tests
- [ ] Docker containerization
- [ ] Rest API for remote monitoring

---

## 📝 License

This project is open-source and available under the **MIT License**. See `LICENSE` file for details.

---

## 🤝 Contributing

Found a bug? Have a feature idea? Contributions welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Open a pull request

---

## 📬 Contact

Built with ❤️ by [Akshaj Goel](https://aksweb.me)

- **Email:** akshajgoel@bnpsramvihar.edu.in
- **GitHub:** [@aksgamigg](https://github.com/aksgamigg)
- **Portfolio:** [aksweb.me](https://aksweb.me)
- **Instagram:** [@aksgamig](https://instagram.com/aksgamig)

---

## 🎓 About the Developer

🇮🇳 10th Grade Student | 🎯 MIT Bound | 💻 Full-Stack Developer

Building privacy-first software and studying AI/neural networks. Passionate about open-source, software architecture, and making technology accessible.

**Current Focus:**
- Python & GUI development
- Algorithms & data structures
- AI/ML fundamentals
- CBSE Class 10 Board exams

---

**© 2025 Akshaj Goel. Code is Poetry.**

*Last Updated: 17 December 2025*

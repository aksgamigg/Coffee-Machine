from gtts import gTTS
import pygame
import tempfile
import os
import threading

class CoffeeMachine:
    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
            "money": 20.0
        }
        self.MENU = {
            "espresso": {
                "ingredients": {
                    "water": 50,
                    "coffee": 18,
                },
                "cost": 1.5,
            },
            "latte": {
                "ingredients": {
                    "water": 200,
                    "milk": 150,
                    "coffee": 24,
                },
                "cost": 2.5,
            },
            "cappuccino": {
                "ingredients": {
                    "water": 250,
                    "milk": 100,
                    "coffee": 24,
                },
                "cost": 3.0,
            }
        }

    def refill(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
            "money": 20.0
        }

machine = CoffeeMachine()

def verify_resources(drink_name):
    """
    Checks if resources are sufficient. 
    If yes, deducts them and returns True.
    If no, returns False and the missing ingredient.
    """
    drink = machine.MENU[drink_name]
    ingredients = drink["ingredients"]

    # 1. Check if we have enough first
    for item, amount in ingredients.items():
        if machine.resources[item] < amount:
            return False, item  # Return False and the missing item name

    # 2. If we are here, we have enough. Now subtract.
    for item, amount in ingredients.items():
        machine.resources[item] -= amount

    return True, None


def process_payment(total_cost, no_pennies, no_nickels, no_dimes, no_quarters, no_dollars):
    # Process coins and bills
    try:
        no_pennies = int(no_pennies or 0)
        no_nickels = int(no_nickels or 0)
        no_dimes = int(no_dimes or 0)
        no_quarters = int(no_quarters or 0)
        no_dollars = int(no_dollars or 0)
    except ValueError:
        # Safety net if they type text instead of numbers
        no_pennies = no_nickels = no_dimes = no_quarters = no_dollars = 0
    # Calculate value by multiplying count by coin value
    val_pennies = no_pennies * 0.01
    val_nickels = no_nickels * 0.05
    val_dimes = no_dimes * 0.10
    val_quarters = no_quarters * 0.25

    payment = val_pennies + val_nickels + val_dimes + val_quarters + no_dollars

    # CRITICAL: Round to 2 decimal places to prevent floating-point errors
    payment = round(payment, 2)

    # Check payment
    if payment > machine.resources["money"]:
        return False, None, None
    elif payment >= total_cost:
        change = round(payment - total_cost, 2)
        machine.resources["money"] += payment
        machine.resources["money"] -= change
        return True, change, payment
    else:
        return False, None, payment

def _speak_worker(text):
    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name
        tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.wait(50)

    pygame.mixer.quit()
    os.remove(filename)

def speak(text):
    threading.Thread(
        target=_speak_worker,
        args=(text,),
        daemon=True
    ).start()

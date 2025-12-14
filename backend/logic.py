class CoffeeMachine:
    def __init__(self):
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
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
    # Calculate value by multiplying count by coin value
    val_pennies = no_pennies * 0.01
    val_nickels = no_nickels * 0.05
    val_dimes = no_dimes * 0.10
    val_quarters = no_quarters * 0.25

    payment = val_pennies + val_nickels + val_dimes + val_quarters + no_dollars

    # CRITICAL: Round to 2 decimal places to prevent floating-point errors
    payment = round(payment, 2)

    # Check payment
    if payment >= total_cost:
        change = round(payment - total_cost, 2)
        return True, change
    else:
        return False, None
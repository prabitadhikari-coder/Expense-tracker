import json
import pathlib
# ============================================================
# File Path Setup
# ============================================================

# Path to the directory containing this script
path = pathlib.Path(__file__).parent
# Path to the expenses.json file
data = path / "expenses.json"

# ============================================================
# File Creation
# ============================================================

# Create the JSON file if it does not exist
if not data.exists():
    data.write_text("[]", encoding="utf-8")

else:
    print("File already exists.")
    
# ============================================================
# Custom Exceptions
# ============================================================

class AmountError(Exception):
    """Error related to the expense amount."""
    pass

class OptionError(Exception):
    """Error related to the menu option."""
    pass

class CategoryError(Exception):
    """Error related to the expense category."""
    pass

class JsonError(Exception):
    """Error related to JSON operations."""
    pass

class EmptyFieldError(Exception):
    """Error when a required field is empty."""
    pass

# ============================================================
# Read Expenses from JSON File
# ============================================================
def record_expenses() -> list[dict]:
    """Read expenses from the JSON file."""
    try:
        with open(data, "r", encoding="utf-8") as file:
            expenses = json.load(file)
        return expenses
    except FileNotFoundError:
        # If the file cannot be found, return an empty list.
        return []
    except json.JSONDecodeError as error:
        # The file exists, but the JSON is invalid.
        raise JsonError("The JSON file is not valid.") from error

# ============================================================
# Show Expenses
# ============================================================
def show_expenses(expenses: list[dict]) -> None:
    """Show expenses for a selected month."""
    month = input("Enter the month (YYYY-MM): ")
    total = 0
    # Dictionary to store total expenses for each category
    categories = {}
    found = False
    # Go through every expense
    for expense in expenses:
        # Get YYYY-MM from the date
        expense_month = expense["date"][:7]
        # Check if the expense belongs to the selected month
        if expense_month == month:
            found = True
            # Show the individual expense
            print(
                f"Date: {expense['date']}, "
                f"Category: {expense['category']}, "
                f"Amount: {expense['amount']}"
            )
            # Add amount to the monthly total
            total += expense["amount"]
            # Get the category
            category = expense["category"]
            # Add the amount to the category total
            if category in categories:
                categories[category] += expense["amount"]
            else:
                categories[category] = expense["amount"]
    # ========================================================
    # Display Monthly Results
    # ========================================================
    if not found:
        print(f"No expenses recorded for {month}.")
    else:
        print("\n------------------------------")
        # Show total expenses
        print(f"Total expenses for {month}: {total}")
        # Show category totals
        print("\nExpenses by category:")
        for category, amount in categories.items():
            print(f"{category}: {amount}")
# ============================================================
# Save Expenses to JSON File
# ============================================================
def save_expenses(expenses: list[dict]) -> None:
    """Save expenses to the JSON file."""
    try:
        with open(data, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)
    except OSError as error:
        raise JsonError(
            "Failed to update the JSON file."
        ) from error
    else:
        print("Expenses updated successfully.")
# ============================================================
# Add New Expense
# ============================================================

def add_expense() -> None:
    """Ask the user for an expense and save it."""
    # ========================================================
    # Ask for the Amount
    # ========================================================
    while True:
        try:
            amount_input = input(
                "Enter the expense amount: "
            )
            # Check if the field is empty
            if not amount_input:
                raise EmptyFieldError(
                    "Amount cannot be empty."
                )
            # Convert the input into a number
            amount = float(amount_input)
            # Amount must be greater than zero
            if amount <= 0:
                raise AmountError(
                    "Amount must be greater than zero."
                )
            break
        except ValueError:
            print(
                "Invalid input. "
                "Please enter a numeric value."
            )
        except AmountError as error:
            print(error)
        except EmptyFieldError as error:
            print(error)
    # ========================================================
    # Ask for the Category
    # ========================================================

    while True:
        try:
            category = input(
                "Enter the expense category "
                "(Food, Transportation, Entertainment): "
            )
            # Check if the field is empty
            if not category:
                raise EmptyFieldError(
                    "Category cannot be empty."
                )
        #     # Check if the category is valid
        #     if category not in [
        #         "Food",
        #         "Transportation",
        #         "Entertainment"
        #     ]:
        #         raise CategoryError(
        #             "Invalid category."
        #         )
            break
        # except CategoryError as error:
        #     print(error)
        except EmptyFieldError as error:
            print(error)
    # =================================================================
    # Ask for the Date #Needs improvement in Date Validation for future
    # =================================================================
    while True:
        try:
            date = input(
                "Enter the expense date with the correct format "
                "(YYYY-MM-DD) Eg.(2026-01-01): "
            )
            # Check if the field is empty
            if not date:
                raise EmptyFieldError(
                    "Date cannot be empty."
                )
            # Simple date format check
            if (
                len(date) != 10
                or date[4] != "-"
                or date[7] != "-"
            ):
                raise ValueError
            break
        except ValueError:
            print(
                "Invalid date format. "
                "Use YYYY-MM-DD."
            )
        except EmptyFieldError as error:
            print(error)
    # ========================================================
    # Create New Expense
    # ========================================================
    new_expense = {
        "amount": amount,
        "category": category,
        "date": date
    }
    # ========================================================
    # Load Existing Expenses
    # Add New Expense
    # Save Expenses
    # ========================================================
    expenses = record_expenses()
    expenses.append(new_expense)
    save_expenses(expenses)

# ============================================================
# Expense Tracker Menu
# ============================================================
def main() -> None:
    """Run the interactive expense tracker menu."""
    while True:
        print("\n==============================")
        print("       EXPENSE TRACKER")
        print("==============================")
        print("1. Add expense")
        print("2. Show expenses")
        print("3. Exit")
        option = input("Enter your choice: ")
        # ========================================================
        # Handle Menu Option
        # ========================================================
        try:
            if option == "1":
                add_expense()
            elif option == "2":
                expenses = record_expenses()
                show_expenses(expenses)
            elif option == "3":
                print("Goodbye!")
                break
            else:
                raise OptionError(
                    "Invalid input. "
                    "Please choose 1, 2, or 3."
                )
        except OptionError as error:
            print(error)
        except JsonError as error:
            print(f"File error: {error}")


if __name__ == "__main__":
    main()
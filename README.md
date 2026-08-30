# Expense Tracker

A simple Python program for recording and viewing personal expenses.

## Features

* Add a new expense
* Enter the expense amount, category, and date
* Save expenses automatically in a JSON file
* View expenses for a specific month
* See the total amount spent in a month
* See expenses grouped by category
* Handles invalid input and errors

## Requirements

You only need:

* Python 3
* No external libraries are required

The program uses Python's built-in `json` and `pathlib` modules.

## How to Run

1. Make sure Python is installed on your computer.
2. Put `expense_tracker.py` in a folder.
3. Open Command Prompt or PowerShell in that folder.
4. Run:

```bash
python expense_tracker.py
```

The program will automatically create an `expenses.json` file if it does not already exist.

## Main Menu

When the program starts, you will see:

```text
==============================
       EXPENSE TRACKER
==============================
1. Add expense
2. Show expenses
3. Exit
```

### 1. Add Expense

Choose **1** to add a new expense.

You will be asked for:

**Amount**

```text
Enter the expense amount:
```

Enter a positive number, for example:

```text
25.50
```

**Category**

```text
Enter the expense category (Food, Transportation, Entertainment):
```

For example:

```text
Food
```

**Date**

```text
Enter the expense date with the correct format (YYYY-MM-DD)
```

For example:

```text
2026-08-30
```

The expense is then saved to `expenses.json`.

## 2. Show Expenses

Choose **2** to view expenses.

The program asks for a month in this format:

```text
YYYY-MM
```

For example:

```text
2026-08
```

It will display the expenses recorded during that month and show:

* Individual expenses
* Total expenses
* Total spent in each category

Example:

```text
Date: 2026-08-05, Category: Food, Amount: 15.0
Date: 2026-08-10, Category: Transportation, Amount: 20.0

------------------------------
Total expenses for 2026-08: 35.0

Expenses by category:
Food: 15.0
Transportation: 20.0
```

## 3. Exit

Choose **3** to close the program.

```text
Goodbye!
```

## Data Storage

The program stores your expenses in:

```text
expenses.json
```

The file is created automatically if it does not exist.

The data is stored in JSON format, for example:

```json
[
    {
        "amount": 15.0,
        "category": "Food",
        "date": "2026-08-30"
    }
]
```

## Error Handling

The program checks for several common mistakes, such as:

* Empty amount
* Empty category
* Empty date
* Amount that is zero or negative
* Non-numeric amount
* Incorrect date format
* Invalid menu option
* Problems reading or saving the JSON file

For example, entering:

```text
abc
```

as the amount will show an error instead of crashing the program.

## Project Structure

```text
Expense Tracker/
│
├── expense_tracker.py
└── expenses.json
```

`expense_tracker.py` contains the main program.

`expenses.json` contains your saved expenses.

## Important Notes and Limitations

Please keep the following limitations in mind when using the Expense Tracker:

* **Date validation is basic:** The program only checks whether the date follows the `YYYY-MM-DD` format. It does not completely verify whether the entered date is a real calendar date.

* **No editing or deleting expenses:** Once an expense is saved, the program does not currently provide an option to edit or delete it.

* **No duplicate checking:** The program does not check whether the same expense has already been entered, so duplicate expenses can be recorded.

* **Categories are not strictly controlled:** Although the program suggests `Food`, `Transportation`, and `Entertainment`, users can currently enter other category names as well.

* **No currency selection:** The program does not allow users to select or change the currency. The amount is simply stored as a number.

* **No user accounts:** There is no login or user-account system. Anyone who can access the program and its files can use the expense tracker.

* **Local data storage:** Expenses are stored in a local `expenses.json` file. The program does not use an online database or cloud storage.

* **No automatic backup:** The program does not create backups of the `expenses.json` file. If the file is accidentally deleted or damaged, the saved expenses may be lost.

* **No advanced reports:** The program only provides monthly totals and totals by category. It does not currently generate charts, graphs, yearly reports, or spending trends.

* **Limited search and filtering:** Expenses can only be viewed by entering a specific month. There are no options to search by individual date, amount, or category.

* **No budget tracking:** The program does not allow users to set a monthly budget or receive warnings when spending exceeds a budget.

* **No income tracking:** The program is designed only for expenses. It does not record income or calculate savings/profit.

* **Simple command-line interface:** The application runs in the terminal/command prompt and does not have a graphical user interface.

* **JSON file dependency:** The program relies on the `expenses.json` file for storing data. If the JSON file becomes invalid or corrupted, the program may not be able to read the saved expenses.

These limitations are expected for a simple beginner-level expense tracking application and can be improved in future versions.

## Author

Expense Tracker — Python Project - Prabit Adhikari

# Expense Tracker (Version 1)

A simple desktop Expense Tracker built using **Python** and **Tkinter** that allows users to record, edit, delete, and search expenses. The application follows an object-oriented design with separate modules for the GUI, business logic, storage, and expense model.

---

##  Features

-  Add new expenses
-  Edit existing expenses
-  Delete expenses
-  Search by:
  - Description (case-insensitive)
  - Category
-  Persistent storage using SQLite
-  Displays:
  - Total expenses
  - Number of expenses
-  User-friendly Tkinter GUI with Treeview
- Bar and pie graphs

---

##  Technologies Used

- Python 3
- Tkinter
- SQLite
- matplotlib
- Object-Oriented Programming (OOP)


## Project Structure

Expense Tracker/
expense.py              # Expense model
expenseManager.py       # Business logic
expensestorage.py       # JSON storage handling
expenseGUI.py           # Main GUI controller
expense_statistics.py   # Analytical graphs
fixed_constants.py      # Categories and constants
exepense.db             # Expense database (ignored by Git)
.gitignore
requirements.txt
README.md


##  Architecture

The project follows a modular architecture.

ExpenseGUI->ExpenseManage->ExpenseStorage (SQlite)

ExpenseGUI:
Header Section
Search Section
Expense List (Treeview)
Action Buttons
Expense Popup


Each class has a single responsibility, making the code easier to understand and maintain.



##  Planned Features (Version 2)
 
- Expense Sorting
- Filter by Date Range
- Mini calendar to choose the date instead of typing it manuallygit sta


##  What I Learned

This project helped me improve my understanding of:

- Object-Oriented Programming
- Tkinter GUI Development
- Event-driven Programming
- JSON File Handling
- SQlite database management
- matplotlib
- Software Architecture
- Git & GitHub
- Modular Program Design

By Jiteeshkumar
CSE student


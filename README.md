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
-  Persistent storage using JSON
-  Displays:
  - Total expenses
  - Number of expenses
-  User-friendly Tkinter GUI with Treeview

---

##  Technologies Used

- Python 3
- Tkinter
- JSON
- Object-Oriented Programming (OOP)


## Project Structure

Expense Tracker/
expense.py              # Expense model
expenseManager.py       # Business logic
expensestorage.py       # JSON storage handling
expenseGUI.py           # Main GUI controller
fixed_constants.py      # Categories and constants
database.json           # Expense database (ignored by Git)
.gitignore
README.md


##  Architecture

The project follows a modular architecture.

ExpenseGUI->ExpenseManage->ExpenseStorage (JSON)

ExpenseGUI:
Header Section
Search Section
Expense List (Treeview)
Action Buttons
Expense Popup


Each class has a single responsibility, making the code easier to understand and maintain.



##  Planned Features (Version 2)

- SQLite Database
- Graphs 
- Date Validation
- Expense Sorting
- Filter by Date Range


##  What I Learned

This project helped me improve my understanding of:

- Object-Oriented Programming
- Tkinter GUI Development
- Event-driven Programming
- JSON File Handling
- Software Architecture
- Git & GitHub
- Modular Program Design

By Jiteeshkumar
CSE student


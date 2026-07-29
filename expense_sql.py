import sqlite3
from expense import Expense
class SQL_DataManager:
    def __init__(self):
        self.database="expenses.db"
        connection=sqlite3.connect(self.database)
        cursor=connection.cursor()
        query="CREATE TABLE IF NOT EXISTS Expenses(id INTEGER PRIMARY KEY, description TEXT NOT NULL, amount REAL NOT NULL, category TEXT NOT NULL, date TEXT NOT NULL);"
        cursor.execute(query)
        connection.commit()
        connection.close()
    def connect(self):
        return sqlite3.connect(self.database)
    def create_expense_object(self,data):
        expenses=[]
        for i in data:
            expense=Expense(i[0],i[1],i[2],i[3],i[4])
            expenses.append(expense)
        return expenses
    def get_all_expenses(self):
        connection=self.connect()
        cursor = connection.cursor()
        query="SELECT * FROM Expenses;"
        cursor.execute(query)
        data=cursor.fetchall()
        return self.create_expense_object(data)
    def insert_expenses(self,description,amount,category,date):
        connection = self.connect()
        cursor = connection.cursor()
        query = "INSERT INTO Expenses(description, amount, category, date) VALUES (?, ?, ?, ?);"
        values = (description,amount,category,date)
        cursor.execute(query, values)
        expense_id =cursor.lastrowid
        connection.commit()
        connection.close()
        return expense_id
    def delete_expenses(self,expense_id):
        connection = self.connect()
        cursor = connection.cursor()
        query="DELETE FROM Expenses WHERE id=?;"
        values=(expense_id,)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
        return True
    def update_expense(self,expense):
        connection = self.connect()
        cursor = connection.cursor()
        query="UPDATE Expenses SET description=?,amount=?,category=?,date=? WHERE id=?"
        values=(expense.description,expense.amount,expense.category,expense.date,expense.id)
        cursor.execute(query,values)
        connection.commit()
        connection.close()
        return True
    def sort_expense(self,attribute,order_asc=True):
        connection = self.connect()
        cursor = connection.cursor()
        if attribute in ("amount","date") and order_asc==True:
            query=f"SELECT * FROM Expenses ORDER BY {attribute} ASC "
            cursor.execute(query)
            data=cursor.fetchall()
            connection.close()
            return self.create_expense_object(data)
        elif attribute in ("amount","date") and order_asc==False:
            query=f"SELECT * FROM Expenses ORDER BY {attribute} DESC "
            cursor.execute(query)
            data=cursor.fetchall()
            connection.close()
            return self.create_expense_object(data)
        else:
            return
    def amount_by_range(self,min_amount,max_amount):
        connection = self.connect()
        cursor = connection.cursor()
        query="SELECT * FROM Expenses WHERE amount BETWEEN ? AND ?"
        values=(min_amount,max_amount)
        cursor.execute(query,values)
        data=cursor.fetchall()
        connection.close()
        return self.create_expense_object(data)
    def date_by_range(self,min_date,max_date):
        connection = self.connect()
        cursor = connection.cursor()
        query="SELECT * FROM Expenses WHERE date BETWEEN ? AND ?"
        values=(min_date,max_date)
        cursor.execute(query,values)
        data=cursor.fetchall()
        connection.close()
        return self.create_expense_object(data)

    


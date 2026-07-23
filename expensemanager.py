import expensestorage as es
from expense import Expense
from fixed_constants import Valid_categories
class ExpenseManager:
    def __init__(self):
        expenses_data=es.load_database()
        self.next_id=expenses_data['next_id']
        self.expenses=[]
        for expense_dict in expenses_data['expenses']:
            expense=Expense(expense_dict)
            self.expenses.append(expense)
    def add_expense(self,amount,category,description,date):
        if category in Valid_categories:
            if amount>0:
                expense_dict={"id":self.next_id,"amount":amount,"category":category,"description":description,"date":date}
                expense=Expense(expense_dict)
                self.expenses.append(expense)
                self.next_id+=1
                self.save_expenses()
                
                return True,"SUCCESS"
            else:
                return False,"AMOUNT_NEGATIVE"
        else:
            return False,"INVALID_CATEGORY"    
    def get_total_expense(self):
        total_amount=0
        for i in self.expenses:
            total_amount+=i.amount
        return total_amount
    def get_expense_by_id(self,expense_id):
        for i in self.expenses:
            if i.id==expense_id:
                return i,"SUCCESS"
        else:
            return None,"NOT_FOUND"    
    def del_expense(self,expense_id):
        expense,status=self.get_expense_by_id(expense_id)
        if status=="SUCCESS":
            self.expenses.remove(expense)
            self.save_expenses()
            return True,"DELETE_SUCCESS"
        else:
            return False,"NOT_FOUND"
    def edit_expense(self,expense_id,amount=None,category=None,description=None,date=None):
        expense, status=self.get_expense_by_id(expense_id)
        if status=="SUCCESS":
            if amount is not None and amount>=0:
                expense.amount=amount
            if category is not None and category in Valid_categories:
                expense.category=category
            if description is not None:
                expense.description=description
            if date is not None:
                expense.date=date
            self.save_expenses()
            return True,"EDIT_SUCCESS"
        else:
            return False,"NOT_FOUND"
    def search(self,attribute,value):
        result=[]
        for i in self.expenses:
            if getattr(i,attribute)==value:
                result.append(i)
        return result
    def search_by_category(self,category):
        return self.search('category',category)
    def search_by_amount(self,amount):
        return self.search('amount',amount)
    def search_by_description(self,description):
        return self.search('description',description)
    def search_by_date(self,date):
        return self.search('date',date)
    def get_existing_category(self):
        category_list=set()
        for i in self.expenses:
            category_list.add(i.category)
        return list(category_list)
    def get_all_dates(self):
        date_list=set()
        for i in self.expenses:
            date_list.add(i.date)
        return list(date_list)
    def get_no_of_expenses(self):
        return len(self.expenses)
    def save_expenses(self):
        data={'next_id':self.next_id,'expenses':[i.create_dict() for i in self.expenses]}
        es.write_database(data)
    def search_by_description_and_category(self,description,category="All"):
        result=[]
        if category=="All":
            for i in self.expenses:
                if (i.description).lower()==description.lower() or description.lower() in (i.description).lower():
                    result.append(i)
        else:
            for i in self.expenses:
                if (i.description).lower()==description.lower() or description.lower() in (i.description).lower() and i.category==category:
                    result.append(i)
        return result
   
    
        
        
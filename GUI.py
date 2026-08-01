import tkinter as tk
from tkinter import messagebox
from expensemanager import ExpenseManager
from tkinter import ttk
from fixed_constants import Valid_categories

class ExpenseGUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("600x600")
        self.root.resizable(False,False)
        self.root.title("Expense Tracker")
        self.em=ExpenseManager()
        self.header_section=HeaderSection(self.root)
        self.search_section=SearchSection(self.root,self)
        self.expense_treeview=Expense_List_Section(self.root)
        self.expense_action=ActionWidgets(self.root,self)
        
        self.refresh_header()
        self.expense_treeview.refresh(self.em.expenses)
    def refresh_header(self):
        total_expense=self.em.get_total_expense()
        no_of_expenses=self.em.get_no_of_expenses()
        self.header_section.refresh(total_expense,no_of_expenses)    
    def add_expense(self):
        expense_popup = Expense_Popup(self.root)
        self.root.wait_window(expense_popup.popup)
        if expense_popup.data is not None:
            amount, category, description, date = expense_popup.data
            status,reason=self.em.add_expense(amount,category,description,date)
            if status:
                self.refresh_header()
                self.expense_treeview.refresh(self.em.expenses)
            else:
                messagebox.showwarning("Error",f"{reason}")
    def edit_expense(self):
        selected_id = self.expense_treeview.tree.selection()
        if selected_id==():
            messagebox.showwarning(title="Error",message="please select an expense")
            return
        expense=self.em.get_expense_by_id(int(selected_id[0]))
        expense_popup=Expense_Popup(self.root,expense[0])
        expense_popup.edit_expense()
        self.root.wait_window(expense_popup.popup)
        if expense_popup.data is not None:
            amount, category, description, date = expense_popup.data
            self.em.edit_expense(int(selected_id[0]),amount,category,description,date)
            self.refresh_header()
            self.expense_treeview.refresh(self.em.expenses)
    def delete_expense(self):
        selected_id = self.expense_treeview.tree.selection()
        if selected_id==():
            messagebox.showwarning("Error",message="please select an expense")
            return
        self.em.del_expense(int(selected_id[0]))
        self.refresh_header()
        self.expense_treeview.refresh(self.em.expenses)
    def clear_search(self):
        self.search_section.desc_entry.delete(0,tk.END)
        self.search_section.category_box.set("All")
        self.expense_treeview.refresh(self.em.expenses)
    def search_expense(self):
        search_desc=self.search_section.desc_entry.get()
        search_category=self.search_section.category_box.get()
        if search_desc=="" and search_category=="All":
            self.expense_treeview.refresh()
        search_results=self.em.search_by_description_and_category(description=search_desc,category=search_category)
        self.expense_treeview.refresh_by_search(search_results)
    def get_existing_category(self):
        return self.em.get_existing_category()
    def execute_pie_chart(self):
        self.em.execute_pie_chart()
    def execute_bar_chart(self):
        self.em.execute_bar_chart()
    def Statistics_popup_open(self):
        self.Statistics_popup=Statistics_Popup(self.root,self)
        self.root.wait_window(self.Statistics_popup.popup)
    def run(self):
        self.header_section
        self.search_section
        self.expense_treeview
        self.expense_action
        self.root.mainloop()



    
class HeaderSection:
    def __init__ (self,parent):
        self.label_title=tk.Label(parent,text="Expense Tracker")
        self.total_expense=tk.Label(parent,text="Total Expense: $0.00")
        self.no_of_expense=tk.Label(parent,text="Number of Expenses: 0")
        self.label_title.grid(row=0, column=0, columnspan=2, padx=(150,150),pady=20)
        self.total_expense.grid(row=1, column=0, sticky="w", padx=10)
        self.no_of_expense.grid(row=1, column=1, sticky="e", padx=10)
    def refresh(self,total_expense,no_of_expense):
        self.total_expense.config(text=f"Total Expense: ${total_expense:.2f}")
        self.no_of_expense.config(text=f"Number of Expenses: {no_of_expense}")
    
class SearchSection:
    def __init__(self,parent,controller):
        self.controller=controller
        self.desc_name=tk.Label(parent,text="description:")
        self.desc_entry=tk.Entry(parent)
        self.search_button=tk.Button(parent,text="Search",command=self.controller.search_expense)
        self.clear_button=tk.Button(parent,text="Clear",command=self.controller.clear_search)
        self.cat_name=tk.Label(parent,text="category:")
        self.category_box=ttk.Combobox(parent,state="readonly")
        self.category_box.set("All")
        self.category_box['values']=["All"]+self.controller.get_existing_category()
        self.desc_name.grid(row=2, column=0, padx=10, pady=(10, 2), sticky="w")
        self.cat_name.grid(row=2, column=1, padx=10, pady=(10, 2), sticky="w")
        self.desc_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.category_box.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="ew")
        self.search_button.grid(row=3, column=2, padx=(20, 5), pady=(0, 10))
        self.clear_button.grid(row=3, column=3, padx=(5, 10), pady=(0, 10))
    
    
class Expense_List_Section:
    def __init__(self,parent):
        self.tree=ttk.Treeview(parent,columns=("Amount","Category","Description","Date"),show="headings")
        self.tree.heading("Amount",text="Amount")
        self.tree.heading("Category",text="Category")
        self.tree.heading("Description",text="Description")
        self.tree.heading("Date",text="Date")
        self.tree.column("Date",width=100)
        self.tree.column("Category",width=100)
        self.tree.column("Amount",width=100)
        self.tree.column("Description",width=200)
        self.tree.grid(row=4,column=0,columnspan=4,padx=10,pady=10,sticky="nsew")
    def refresh(self,expenses):
        self.tree.delete(*self.tree.get_children())
        for i in expenses:
            self.tree.insert("","end",iid=i.id,values=(i.amount,i.category,i.description,i.date))
    def refresh_by_search(self,results):
        self.tree.delete(*self.tree.get_children())
        for i in results:
            self.tree.insert("","end",iid= i.id,values=(i.amount,i.category,i.description,i.date))

class ActionWidgets:
    def __init__(self,parent,controller):
        self.controller=controller
        self.add_button=tk.Button(parent,text="Add Expense",command=self.controller.add_expense)
        self.edit_button=tk.Button(parent,text="Edit Expense",command=self.controller.edit_expense)
        self.delete_button=tk.Button(parent,text="Delete Expense",command=self.controller.delete_expense)
        self.statics_button=tk.Button(parent,text="Statistics",command=self.controller.Statistics_popup_open)
        self.add_button.grid(row=5,column=0,padx=5,pady=10)
        self.edit_button.grid(row=5,column=1,padx=5,pady=10)
        self.delete_button.grid(row=5,column=2,padx=5,pady=10)
        self.statics_button.grid(row=5,column=3,padx=5,pady=10)
        

class Expense_Popup:
    def __init__(self,parent,expense=None):
        self.popup=tk.Toplevel(parent)
        self.expense=expense
        self.title_popup=tk.Label(self.popup,text="")
        if self.expense==None:
            self.title_popup.config(text="Add Expense")
        else:
            self.title_popup.config(text="Edit Expense")
        self.amount_name=tk.Label(self.popup,text="Amount:")
        self.amount_popup=tk.Entry(self.popup)
        self.category_box_popup=ttk.Combobox(self.popup,state="readonly")
        self.category_box_popup['values']=Valid_categories
        self.categ_name=tk.Label(self.popup,text="Category:")
        self.desc_name=tk.Label(self.popup,text="Description:")
        self.desc_popup=tk.Entry(self.popup)
        self.date_name=tk.Label(self.popup,text="Date:")
        self.date_popup=tk.Entry(self.popup)
        self.save_button=tk.Button(self.popup,text="Save",command=self.save)
        self.cancel_button=tk.Button(self.popup,text="cancel",command=self.cancel)
        self.title_popup.grid(row=0,column=0,columnspan=2,pady=(10, 20))
        self.amount_name.grid(row=1,column=0, padx=10,pady=5,sticky="w")
        self.amount_popup.grid(row=1, column=1,padx=10,pady=5,sticky="ew")
        self.categ_name.grid(row=2,column=0,padx=10,pady=5,sticky="w")
        self.category_box_popup.grid(row=2,column=1,padx=10,pady=5,sticky="ew")
        self.desc_name.grid(row=3,column=0,padx=10,pady=5,sticky="w")
        self.desc_popup.grid(row=3,column=1,padx=10,pady=5,sticky="ew")
        self.date_name.grid(row=4,column=0,padx=10,pady=5,sticky="w")
        self.date_popup.grid(row=4,column=1,padx=10,pady=5,sticky="ew")
        self.save_button.grid(row=5,column=0)
        self.cancel_button.grid(row=5,column=1)
        self.popup.protocol("WM_DELETE_WINDOW", self.cancel)
        self.data=None
    def save(self):
        self.data=self.get_data()
        self.popup.destroy()
        
    def cancel(self):
        self.popup.destroy()
    def get_data(self):
        amount=int(self.amount_popup.get())
        category=self.category_box_popup.get()
        description=self.desc_popup.get()
        date=self.date_popup.get()
        if amount>0:
            if category in Valid_categories:
                if description != "" and date !="":
                    return amount,category,description,date
                else:
                    messagebox.showwarning(title="Error",message="Invalid description or date")
                    return
            else:
                messagebox.showwarning(title="Error",message="Enter a Valid Category")
                return
        else:
            messagebox.showwarning(title="Error",message="Enter a valid amount")
            return
            
    def edit_expense(self):
        amount=self.expense.amount
        category=self.expense.category
        description=self.expense.description
        date=self.expense.date
        self.amount_popup.insert(0,amount)
        self.category_box_popup.set(category)
        self.desc_popup.insert(0,description)
        self.date_popup.insert(0,date)

class Statistics_Popup:
    def __init__(self,parent,controller):
        self.popup=tk.Toplevel(parent)
        self.popup.geometry("300x250")
        self.controller=controller
        self.title_popup=tk.Label(self.popup,text="Statistics")
        self.pie_chart_button=tk.Button(self.popup,text="Pie Chart",command=self.controller.execute_pie_chart)
        self.bar_chart_button=tk.Button(self.popup,text="Bar Chart",command=self.controller.execute_bar_chart)
        self.title_popup.grid(row=0,column=0,columnspan=2,pady=(10, 20))
        self.pie_chart_button.grid(row=1,column=0,padx=10,pady=5,sticky="ew")
        self.bar_chart_button.grid(row=1,column=1,padx=10,pady=5,sticky="ew")
        











        
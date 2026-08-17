import tkinter as tk
from tkinter import messagebox
from expensemanager import ExpenseManager
from tkinter import ttk
from fixed_constants import Valid_categories

class ExpenseGUI:
    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("650x600")
        self.root.resizable(False,False)
        self.root.title("Expense Tracker")
        self.em=ExpenseManager()
        self.header_section=HeaderSection(self.root)
        self.filter_section=FilterSection(self.root,self)
        self.expense_treeview=Expense_List_Section(self.root)
        self.expense_action=ActionWidgets(self.root,self)
        self.filter_active=None
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
                self.refresh_expense_view()
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
            self.refresh_expense_view()
    def delete_expense(self):
        selected_id = self.expense_treeview.tree.selection()
        if selected_id==():
            messagebox.showwarning("Error",message="please select an expense")
            return
        self.em.del_expense(int(selected_id[0]))
        self.refresh_header()
        self.refresh_expense_view()
    def clear_filter(self):
        self.expense_treeview.refresh(self.em.expenses)
        self.filter_active=None
    def filter_expenses(self,Entries):
        self.filter_active=Entries
        
        if Entries['category']=="All":
            Entries['category']=None
        if Entries['description']=="":
            Entries['description']=None
        if Entries['min_amount']=="":
            Entries['min_amount']=None
        if Entries['max_amount']=="":
            Entries['max_amount']=None
        if Entries['min_date']=="":
            Entries['min_date']=None
        if Entries['max_date']=="":
            Entries['max_date']=None
        filter_results=self.em.filter_expenses(Entries)
        self.expense_treeview.refresh_by_search(filter_results)
        return filter_results
        
    def show_filter_frame(self):
        self.filter_frame=FilterFrame(self.root,self)
        self.expense_action.filter_button.config(text="Hide Filter",command=self.hide_filter_frame)
        self.filter_frame.grid(row=3,column=0,columnspan=4,padx=10,pady=10,sticky="nsew")
    def hide_filter_frame(self):
        self.filter_frame.grid_forget()
        self.expense_action.filter_button.config(text="Filter",command=self.show_filter_frame)
    def get_existing_category(self):
        return self.em.get_existing_category()
    def refresh_expense_view(self):
        if self.filter_active is not None:
            filter_results=self.filter_expenses(self.filter_active)
            self.expense_treeview.refresh_by_search(filter_results)
        else:
            self.expense_treeview.refresh(self.em.expenses)


    def execute_pie_chart(self):
        self.em.execute_pie_chart()
    def execute_bar_chart(self):
        self.em.execute_bar_chart()
    def Statistics_popup_open(self):
        self.Statistics_popup=Statistics_Popup(self.root,self)
        self.root.wait_window(self.Statistics_popup.popup)
    def run(self):
        self.header_section
        self.filter_section
        self.expense_treeview
        self.expense_action
        self.root.mainloop()



    
class HeaderSection:
    def __init__ (self,parent):
        self.label_title=tk.Label(parent,text="Expense Tracker")
        self.total_expense=tk.Label(parent,text="Total Expense: $0.00")
        self.no_of_expense=tk.Label(parent,text="Number of Expenses: 0")
        self.label_title.grid(row=0, column=0, columnspan=2, padx=(250,150),pady=20)
        self.total_expense.grid(row=1, column=0, sticky="w", padx=10)
        self.no_of_expense.grid(row=1, column=2, sticky="e", padx=10)
    def refresh(self,total_expense,no_of_expense):
        self.total_expense.config(text=f"Total Expense: ${total_expense:.2f}")
        self.no_of_expense.config(text=f"Number of Expenses: {no_of_expense}")
    
class FilterSection:
    def __init__(self,parent,controller):
        self.controller=controller 
        self.desc_entry=tk.Entry(parent)
        self.max_amount_entry=tk.Entry(parent)
        self.min_amount_entry=tk.Entry(parent)
        self.max_date_entry=tk.Entry(parent)
        self.min_date_entry=tk.Entry(parent)
        self.category_box=ttk.Combobox(parent,state="readonly")
        self.category_box.set("All")
        self.category_box['values']=["All"]+self.controller.get_existing_category()
        
    
    
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
        self.filter_button=tk.Button(parent,text="Filter",command=self.controller.show_filter_frame)
        self.add_button.grid(row=5,column=0,padx=5,pady=10,sticky="ew")
        self.edit_button.grid(row=5,column=1,padx=5,pady=10,sticky="ew")
        self.delete_button.grid(row=5,column=2,padx=5,pady=10,sticky="ew")
        self.statics_button.grid(row=6,column=0,padx=5,pady=10,sticky="ew")
        self.filter_button.grid(row=6,column=1,padx=5,pady=10,sticky="ew")
        

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
        self.popup.geometry("250x250")
        self.controller=controller
        self.title_popup=tk.Label(self.popup,text="Statistics")
        self.pie_chart_button=tk.Button(self.popup,text="Pie Chart",command=self.controller.execute_pie_chart)
        self.bar_chart_button=tk.Button(self.popup,text="Bar Chart",command=self.controller.execute_bar_chart)
        self.title_popup.grid(row=0,column=0,columnspan=2,pady=(10, 20))
        self.pie_chart_button.grid(row=1,column=0,padx=20,pady=10,sticky="w")
        self.bar_chart_button.grid(row=1,column=1,padx=20,pady=10,sticky="e")

class FilterFrame(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent)
        self.controller=controller
        self.entries_frame=FilterSection(self,controller)
        self.desc_name=tk.Label(self,text="Description:")
        self.cat_name=tk.Label(self,text="Category:")
        self.max_amount_name=tk.Label(self,text="Max Amount:")
        self.min_amount_name=tk.Label(self,text="Min Amount:")
        self.max_date_name=tk.Label(self,text="Max Date:")
        self.min_date_name=tk.Label(self,text="Min Date:")
        self.desc_name.grid(row=1, column=0, padx=10, pady=(10, 2), sticky="w")
        self.entries_frame.desc_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        self.cat_name.grid(row=1, column=2, padx=10, pady=(10, 2), sticky="w")
        self.entries_frame.category_box.grid(row=1, column=3, padx=10, pady=(0, 10), sticky="ew")
        self.max_amount_name.grid(row=2, column=2, padx=10, pady=(10, 2), sticky="w")
        self.entries_frame.max_amount_entry.grid(row=2, column=3, padx=10, pady=(0, 10), sticky="ew")
        self.min_amount_name.grid(row=2, column=0, padx=10, pady=(10, 2), sticky="w")
        self.entries_frame.min_amount_entry.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew")
        self.max_date_name.grid(row=3, column=2, padx=10, pady=(10, 2), sticky="w")
        self.entries_frame.max_date_entry.grid(row=3, column=3, padx=10, pady=(0, 10), sticky="ew")
        self.min_date_name.grid(row=3, column=0, padx=10, pady=(10, 2), sticky="w")
        self.entries_frame.min_date_entry.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="ew")
        self.filter_button=tk.Button(self,text="Apply Filter",command=self.apply_filter)
        self.clear_filter_button=tk.Button(self,text="Clear Filter",command=self.clear_filter_clicked)
        self.clear_filter_button.grid(row=4, column=2, padx=5, pady=10)
        self.filter_button.grid(row=4, column=3, padx=5, pady=10)
    def apply_filter(self):
        category=self.entries_frame.category_box.get()
        description=self.entries_frame.desc_entry.get()
        min_amount=self.entries_frame.min_amount_entry.get()
        max_amount=self.entries_frame.max_amount_entry.get()
        min_date=self.entries_frame.min_date_entry.get()
        max_date=self.entries_frame.max_date_entry.get()
        Entries={
            'category':category,
            'description':description,
            'min_amount':min_amount,
            'max_amount':max_amount,
            'min_date':min_date,
            'max_date':max_date
        }
        self.controller.filter_expenses(Entries)
        

        
    def clear_filter_clicked(self):
        self.entries_frame.desc_entry.delete(0,tk.END)
        self.entries_frame.category_box.set("All")
        self.entries_frame.max_amount_entry.delete(0,tk.END)
        self.entries_frame.min_amount_entry.delete(0,tk.END)
        self.entries_frame.max_date_entry.delete(0,tk.END)
        self.entries_frame.min_date_entry.delete(0,tk.END)
        self.controller.clear_filter()







        
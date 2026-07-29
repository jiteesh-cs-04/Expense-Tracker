class Expense:
    def __init__(self,id,description,amount,category,date):
        self.amount=amount
        self.id=id
        self.description=description
        self.category=category
        self.date=date
    def create_dict(self):
        expense_dict={"id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date}  
        return expense_dict
        

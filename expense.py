class Expense:
    def __init__(self,expense: dict):
        self.amount=expense['amount']
        self.id=expense['id']
        self.description=expense['description']
        self.category=expense['category']
        self.date=expense['date']
    def create_dict(self):
        expense_dict={"id": self.id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date}  
        return expense_dict
        

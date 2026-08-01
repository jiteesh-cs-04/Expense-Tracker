
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
class Statistics:
    def __init__(self,data):
        self.data=data
    def category_pie_chart(self):
        categories=[i[0] for i in self.data]
        amounts=[i[1] for i in self.data]
        plt.pie(amounts, labels=categories)
        plt.show()
    def monthly_bar_chart(self):
        months=[i[0] for i in self.data]
        amounts=[i[1] for i in self.data]
        plt.bar(months, amounts)
        plt.xlabel("Months")
        plt.ylabel("Amount")
        plt.title("Monthly Expenses")
        plt.show()
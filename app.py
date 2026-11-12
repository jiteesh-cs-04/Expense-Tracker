from flask import Flask, render_template, jsonify,request
from expensemanager import ExpenseManager

app = Flask(__name__)

expense_manager = ExpenseManager()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/expenses", methods=["GET"])
def get_expenses():

    expenses = expense_manager.expenses

    expenses_data = [
        expense.create_dict()
        for expense in expenses
    ]

    return jsonify(expenses_data)

@app.route("/api/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    

    expense_manager.add_expense(
        amount=data["amount"],
        category=data["category"],
        description=data["description"],
        date=data["date"]
    )

    return jsonify({"message": "Expense added successfully"}), 201


@app.route("/api/expenses/edit", methods=["POST"])
def edit_expense():
    data = request.get_json()

    expense_id = int(data["id"])

    amount = float(data["amount"]) if data.get("amount") else None
    description = data.get("description") or None
    category = data.get("category") or None
    date = data.get("date") or None

    success,status=expense_manager.edit_expense(
        expense_id,
        amount=amount,
        description=description,
        category=category,
        date=date
    )
    if not success:
        return jsonify({"message": "Expense ID not found"}), 40

    return jsonify({"message": "Expense updated successfully"}), 200

@app.route("/api/expenses/delete", methods=["POST"])
def delete_expense():
    data = request.get_json()

    expense_id = int(data["id"])

    success, status = expense_manager.del_expense(expense_id)

    if not success:
        return jsonify({"message": "Expense ID not found"}), 404

    return jsonify({"message": "Expense deleted successfully"}), 200


@app.route("/api/expenses/search", methods=["POST"])
def search_expenses():
    data = request.get_json()

    description = data.get("description", "").strip()
    category = data.get("category") or "All"

    if not description and category == "All":
        return jsonify({"message": "Enter a description or select a category"}), 400

    expenses = expense_manager.search_by_description_and_category(
        description,
        category
    )

    expenses_data = [
        expense.create_dict()
        for expense in expenses
    ]

    return jsonify(expenses_data), 200



@app.route("/api/expenses/filter", methods=["POST"])
def filter_expenses():
    data = request.get_json()

    category = data.get("category")
    min_amount = data.get("min_amount")
    max_amount = data.get("max_amount")
    min_date = data.get("min_date")
    max_date = data.get("max_date")

    category = None if category == "All" else category

    min_amount = float(min_amount) if min_amount else None
    max_amount = float(max_amount) if max_amount else None

    expenses = expense_manager.filter_expenses({
        "category": category,
        "min_amount": min_amount,
        "max_amount": max_amount,
        'description': None,
        "min_date": min_date or None,
        "max_date": max_date or None
    })

    expenses_data = [
        expense.create_dict()
        for expense in expenses
    ]

    return jsonify(expenses_data), 200

@app.route("/api/expenses/chart/category", methods=["GET"])
def category_chart():
    data = expense_manager.sql_manager.data_for_pie_chart()

    return jsonify(data)

@app.route("/api/expenses/chart/monthly", methods=["GET"])
def monthly_chart():
    data = expense_manager.sql_manager.data_for_bar_chart()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
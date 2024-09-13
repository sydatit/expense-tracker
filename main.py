import json
from json import JSONEncoder
import argparse
import datetime
import random
import string
from typing import List, Optional
import pandas as pd


class Expense():
    def __init__(self, description, amount, date, id=None, category=None):
        self.description = description
        self.amount = amount
        self.date = date
        self.id = id
        self.category = category

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.id:<5} {self.date:<10} {self.description:<25} ${self.amount:<10}"
    
def main():
    parser = argparse.ArgumentParser(description="Expense Tracker")

    parser.add_argument("action", help="Action to perform", type=str, choices=["add", "list", "summary", "delete", "update", "add_category", "list_category", "export"])
    parser.add_argument('--description', required=False, help="Description of the expense", default="", type=str)
    parser.add_argument('--amount', required=False, help="Amount of the expense", default=0, type=float)
    parser.add_argument('--id', required=False, help="ID of the expense", type=int)
    parser.add_argument('--month', required=False, help="Month of the expense", type=int)
    parser.add_argument('--category', required=False, help="Category of the expense", type=str)

    args = parser.parse_args()

    def to_json(obj):
        return json.dumps(obj, default=lambda obj: obj.__dict__)

    def readExpenses() -> List[Expense]:
        with open('data.json', 'r+', encoding='utf-8') as f:
            try:
                # print('Loading data from file')
                d = json.load(f)
                # print('d:', d)
                # print('type:', type(d[0]))
                listExpenses = list(map(lambda input: Expense.from_dict(input), d))
                if listExpenses is None or listExpenses == []:
                    return []
                return listExpenses
            except Exception as e:
                print('Error loading')
                print(e)
                return None

    def writeExpenses(expenses: List[Expense]):
        with open('data.json', 'w+', encoding='utf-8') as f:
            f.write(to_json(expenses))
    
    def readCategories() -> List[str]:
        try:
            with open('categories.json', 'r+', encoding='utf-8') as f:
                d = json.load(f)
                if d is None:
                    return []
                return d
        except Exception as e:
            print('Error loading')
            print(e)
            return []
    
    def writeCategories(categories: List[str]):
        with open('categories.json', 'w+', encoding='utf-8') as f:
            f.write(json.dumps(categories))

    
    def addNewExpense(amount, description, category: str):
        try:
            if amount <= 0:
                print("Amount must be greater than 0")
                return
            dateTime = datetime.datetime.now()
            newExpense = Expense(description, amount, str(dateTime.date()))

            insertingExpenses = readExpenses()
            maxId = int(max(insertingExpenses, key=lambda x: x.id).id) if insertingExpenses else 0
            newExpense.id = maxId + 1
            newExpense.category = category
            insertingExpenses = [] if insertingExpenses is None else insertingExpenses
            insertingExpenses.append(newExpense)

            # print("json list of expenses", to_json(insertingExpenses))
            writeExpenses(insertingExpenses)
            print(f'Expense added successfully (ID: {newExpense.id})')
        except Exception as e:
            print('Error adding expense')
            print(e)
        

    def listAllExpenses(category: Optional[str]):
        insertingExpenses = readExpenses()
        print(f"{'ID':<5} {'Date':<10} {'Description':<25} {'Amount':<10}")
        for expense in insertingExpenses:
            if category is None:
                print(expense)
            elif expense.category == category:
                print(expense)

    def updateExpense(id, amount, description):
        existExpense = None
        listExpenses = readExpenses()
        for expense in listExpenses:
            if expense.id == id:
                existExpense = expense
                break
        if existExpense is not None:
            existExpense.amount = amount
            existExpense.description = description
            writeExpenses(listExpenses)
            print(f"Expense with id {id} updated successfully")
        else:
            print(f"Expense with id {id} not found")

        
    def deleteExpense(id):
        listExpenses = readExpenses()
        existExpense = None
        for expense in listExpenses:
            if expense.id == id:
                existExpense = expense
                break
        if existExpense is not None:
            listExpenses.remove(existExpense)
            writeExpenses(listExpenses)
            print(f"Expense with id {id} deleted successfully")
        else:
            print(f"Expense with id {id} not found")

    def showSummaryForMonth(month: Optional[int],):
        listExpenses = readExpenses()
        total = 0
        for expense in listExpenses:
            if int(expense.date.split("-")[1]) == month:
                total += expense.amount
            if month is None:
                total += expense.amount
        if month is None:
            print(f"Total expenses: ${total:<10}")
        else:
            # convert month number to month name
            print(f"Total expenses for {datetime.date(2000, month, 1).strftime('%B')}: {total:<10}")

    def addCategory(category: str):
        def checkCategory(category: str):
            if category is None or category == "":
                print("Category name cannot be empty")
                return False
            if len(category.split(" ")) > 1:
                print("Category name cannot contain spaces")
                return False
            return True
        
        if not checkCategory(category):
            # throw exception
            print("Invalid category name")
            return None
        categories = readCategories()
        if category not in categories:
            categories.append(category)
            writeCategories(categories)
            print(f"Category {category} added successfully")
        else:
            print(f"Category {category} already exists")

    def exportExpense():
        try:
            expenses = readExpenses()

            data = dict()
            data['ID'] = [expense.id for expense in expenses]
            data['Date'] = [expense.date for expense in expenses]
            data['Description'] = [expense.description for expense in expenses]
            data['Amount'] = [expense.amount for expense in expenses]
            df = pd.DataFrame(data)
            randomStr = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            currentDate = datetime.datetime.now().strftime("%Y-%m-%d")
            df.to_csv(r"exported_expenses_" + currentDate + "_" + randomStr + ".csv", index=False)
            print("Expenses exported successfully")
        except Exception as e:
            print("Error exporting expenses")
            print(e)
    

    switcher = {
        "add": addNewExpense,
        "list": listAllExpenses,
        "summary": showSummaryForMonth,
        "delete": deleteExpense,
        "update": updateExpense,
        "add_category": addCategory,
        "list_category": lambda: print(readCategories()),
        "export": exportExpense,
    }
    
    myAction = switcher.get(args.action, lambda: print("Invalid action"))

    if args.action == "add":
        myAction(args.amount, args.description, args.category)
    elif args.action == "update":
        myAction(args.id, args.amount, args.description)
    elif args.action == "delete":
        myAction(args.id)
    elif args.action == "summary":
        myAction(args.month)
    elif args.action == "add_category":
        myAction(args.category)
    elif args.action == "list":
        myAction(args.category)
    else:
        myAction()

if __name__ == '__main__':
    main()
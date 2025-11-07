import os
import sys
import json 
import time


monthList=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

FILE="expense.json"
def loadExpenses():
    if not os.path.exists(FILE):
        return []
    with open(FILE,"r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
def saveExpenses(expenses):
    with open(FILE,"w") as f:
        json.dump(expenses,f,indent=4)
def add(description, amount):
    calendarTime=time.ctime()
    timelist=calendarTime.split()
    expenses=loadExpenses()
    expenseNow={"id":len(expenses)+1,"date":calendarTime,"description":description,"amount":amount}
    expenses.append(expenseNow)
    saveExpenses(expenses)
def update(id,description,amount):
    expenses=loadExpenses()
    for data in expenses:
        if data["id"]==id:
            data["description"]=description
            data["amount"]=amount
            data["date"]=time.ctime()
            saveExpenses(expenses)
            return
    print("No such expense found")
def delete(id):
    expenses=loadExpenses()
    newExpenses=[expense for expense in expenses if expense["id"]!=id]
    size=len(newExpenses)
    for i,e in enumerate(newExpenses):
        newExpenses[i]["id"]=i+1
    saveExpenses(newExpenses)
def viewSummary():
    expenses=loadExpenses()
    for expense in expenses:
        for key,value in expense.items():
            print(key,";",value,sep="")
def stripMonth(date):
    newDate=date.split()
    return newDate[1]
def monthlySummary(month):
    expenses=loadExpenses()
    monthSum=[]
    for expense in expenses:
        if stripMonth(expense["date"])==month:
            monthSum.append(expense)
    for expense in monthSum:
        for key,value in expense.items():
            print(key,":",value,sep="")
def showHelp():
    print("""
Usage:
  expense-tracker add [description] [amount]
  expense-tracker summary
  expense-tracker update [id] [new description] [new amount]
  expense-tracker delete [id]
  expense-tracker monthly-summary [Mon]
""")
def main():
    argsize=len(sys.argv)
    if argsize<2:
        print("Command should be of the form 'expense-tracker [add|summary|monthly-summary|update|delete] ...'")
    else:
        command=sys.argv[1]
        if command=="add":
            description=" ".join(sys.argv[2:argsize-1])
            amount=sys.argv[argsize-1]
            add(description,amount)
        elif command=="summary":
            viewSummary()
        elif command=="update":
            amount=sys.argv[-1]
            description=" ".join(sys.argv[3:argsize-1])
            id=int(sys.argv[2])
            update(id,description,amount)
        elif command=="monthly-summary":
            month=sys.argv[2]
            monthlySummary(month)
        elif command=="delete":
            id=int(sys.argv[2])
            delete(id)
        elif command=="showhelp":
            showHelp()

if __name__=="__main__":
    main()

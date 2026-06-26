import csv
from datetime import datetime
import pandas as pd

expenses_file = 'expenses.csv'
id = 'ID'
date = 'date'
description = 'Description'
amount = 'Amount'

monthly_expenses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def is_valid_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False
    
def file_reader():
    try:
        with open(expenses_file, mode='r', encoding='utf-8', newline='') as file:
            if not file.read(1):
                return False, "EMPTY_FILE", None
            else:
                return True, None, list(csv.DictReader(file))
    except FileNotFoundError:
        return False, "FILE_NOT_FOUND", None
    
def file_rewrite(updated_rows):
    try:
        with open(expenses_file, mode='w') as file:
            writer = csv.writer(file)
            writer.writerows(updated_rows)
        return True, None
    except FileNotFoundError:
        return False, "FILE_NOT_FOUND"
    
def file_add_row(new_row):
    try:
        with open(expenses_file, mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        return True, None
    except FileNotFoundError:
        return False, "FILE_NOT_FOUND"

def updateAmount(newAmount, oldAmount, date):
    try:
        month = (datetime.strptime(date, "%Y-%m-%d")).month
    except ValueError:
        return False, "INVALID_DATE"
    try:    
        monthly_expenses[month - 1] -= oldAmount
        monthly_expenses[month - 1] += newAmount
        return True, None
    except ValueError:
        return False, "INVALID_AMOUNT"

def add(args):
    # Validate Inputs
    if not args.amount or args.amount <= 0:
        return False, "INVALID_AMOUNT", None
    
    if not args.description.strip():
        return False, "INVALID_DESCRIPTION", None
    
    if not args.date:
        args.date = (datetime.today().date()).strftime("%Y-%m-%d")
    elif not is_valid_date(args.date):
        return False, "INVALID_DATE", None

    #Read last row to find next ID
    success, error, rows = file_reader()
    if(not success):
        return False, error, None
    
    if not rows:
        next_id = 1
    else:
        last_row = rows[-1]
        try:
            next_id = int(last_row[id]) + 1
        except:
            return False, "FILE_MALFORMED", None

    #Append new row to file
    try:
        new_row = [str(next_id), args.date, args.description, str(args.amount)]
        success, error = file_add_row(new_row)
        if(not success):
            return False, error, None
        
        success, error = updateAmount(args.amount, 0, args.date)
        if success:
            return True, None, next_id
        else:
            return False, error, None
    except Exception:
        return False, "ERROR_SAVING_ROW", None


def update(args):
    # Validate Inputs
    if(not args.id or args.id <= 0):
        return False, "INVALID_ID", None
        
    if(args.amount and args.amount <= 0):
        return False, "INVALID_AMOUNT", None
    
    if(args.description and not args.description.strip()):
        return False, "INVALID_DESCRIPTION", None
    
    #Find matching row and update
    success, error, rows = file_reader()
    if(not success):
        False, error, None

    updated_rows = []
    found = False
    for row in rows:
        try:
            if int(row[id]) == args.id:
                if args.amount: 
                    found = True
                    success, error = updateAmount(args.amount, row[amount], row[date])
                    if success:
                        row[amount] = str(args.amount)
                    else:
                        return False, error, None
                
                if args.description:
                    found = True
                    row[description] = args.description
        except ValueError:
            return False, "FILE_MALFORMED", None

        updated_rows.append(row)   

    #Rewrite file if updated
    if not found:
        return False, "ID_DOESNT_EXIST", None
    else:
        success, error = file_rewrite(updated_rows)
        if (not success):
            return False, error, None
        else:
            return True, None, args.id

def delete(args):
    # Validate inputs
    if(not args.id or args.id <= 0):
        return False, "INVALID_ID", None
    
    #Find matching row and delete
    success, error, rows = file_reader()
    if(not success):
        return False, error, None

    updated_rows = []
    found = False
    for row in rows:
        try:
            if int(row[id]) == args.id:
                found = True
                success, error = updateAmount(0, row[amount], row[date])
                if success:
                    continue
                else:
                    return False, error, None
        except ValueError:
            return False, "FILE_MALFORMED", None
    
        updated_rows.append(row)

    #Rewrite file is updated
    if not found:
        return False, "ID_DOESNT_EXIST", None
    else:
        success, error = file_rewrite(updated_rows)
        if(not success):
            return False, error, None
        else:
            return True, None, args.id

#Get formatted csv
def listExpenses(args):
    success, error, rows = file_reader()
    if(not success):
        return False, error, None

    df = pd.DataFrame(rows)
    return True, None, df

#Get sum
def summary(args):    
    if(not args.month):
        count = sum(monthly_expenses)
        return True, None, count
    elif(args.month <= 0 or args.month > 12):
        return False, "INVALID_MONTH", None
    else:
        count = monthly_expenses[args.month - 1]
        return True, None, count

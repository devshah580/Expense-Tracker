import csv
from datetime import datetime
import pandas as pd
from pathlib import Path
from decimal import Decimal
import error_codes as err_code


expenses_file = 'expenses.csv'
expenseIdHeader = 'ID'
expenseDateHeader = 'Date'
expenseDescriptionHeader = 'Description'
expenseAmountHeader = 'Amount'


def is_valid_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except (ValueError, TypeError):
        return False
    
def initialize_file(file_path):
    if not file_path.is_file():
        with open(expenses_file, "w") as file:
            file.write("ID,Date,Description,Amount")
    elif file_path.stat().st_size == 0:
        new_row = ['ID', 'Date', 'Description', 'Amount']
        file_add_row(new_row)
    
def file_reader():
    file_path = Path(expenses_file)
    initialize_file(file_path)
    
    try:
        with open(expenses_file, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)
                if header != ['ID', 'Date', 'Description', 'Amount']:
                    return False, err_code.ERR_FILE_MALFORMED, None
                else:
                    return True, None, list(csv.DictReader(file))
    except FileNotFoundError:
        return False, err_code.ERR_FILE_NOT_FOUND, None
    
def file_rewrite(updated_rows):
    fieldnames = ['ID', 'Date', 'Description', 'Amount']

    try:
        with open(expenses_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            clean_rows = [row for row in updated_rows if any(field.strip() for field in row)] 
            writer.writerows(clean_rows)
        return True, None
    except FileNotFoundError:
        return False, err_code.ERR_FILE_NOT_FOUND
    
def file_add_row(new_row):
    try:
        with open(expenses_file, mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        return True, None
    except FileNotFoundError:
        return False, err_code.ERR_FILE_NOT_FOUND

def add(args):
    # Validate Inputs
    if not args.amount or args.amount <= 0:
        return False, err_code.ERR_INVALID_AMOUNT, None
    
    if not args.description.strip():
        return False, err_code.ERR_INVALID_DESCRIPTION, None
    
    currDate = args.date
    if not currDate:
        currDate = (datetime.today().date()).strftime("%Y-%m-%d")
    elif not is_valid_date(currDate):
        return False, err_code.ERR_INVALID_DATE, None

    #Read last row to find next ID
    success, error, rows = file_reader()
    if(not success):
        return False, error, None
    
    highest_id = 0
    if rows:
        for row in rows:
            try:
                highest_id = max(highest_id, int(row[expenseIdHeader]) + 1)
            except (ValueError, TypeError):
                return False, err_code.ERR_FILE_MALFORMED, None

    #Append new row to file
    next_id = highest_id + 1
    new_row = [str(next_id), currDate, args.description, str(args.amount)]
    success, error = file_add_row(new_row)
    if(not success):
        return False, error, None
    else:
        return True, None, next_id
        

def update(args):
    # Validate Inputs
    if(not args.id or args.id <= 0):
        return False, err_code.ERR_INVALID_ID, None
        
    if(args.amount is not None and args.amount <= 0):
        return False, err_code.ERR_INVALID_AMOUNT, None
    
    if(args.description and not args.description.strip()):
        return False, err_code.ERR_INVALID_DESCRIPTION, None
    
    #Find matching row and update
    success, error, rows = file_reader()
    if(not success):
        return False, error, None

    updated_rows = []
    updateDone = False
    idFound = False
    for row in rows:
        try:
            if int(row[expenseIdHeader]) == args.id:
                idFound = True
                if args.amount is not None: 
                    updateDone = True
                    row[expenseAmountHeader] = str(args.amount)
                
                if args.description is not None:
                    updateDone = True
                    row[expenseDescriptionHeader] = args.description
        except (ValueError, TypeError):
            return False, err_code.ERR_FILE_MALFORMED, None

        updated_rows.append(row)   

    #Rewrite file if updated
    if not idFound:
        return False, err_code.ERR_ID_DNE, None
    elif not updateDone:
        return False, err_code.ERR_NO_UPDATE, None
    else:
        success, error = file_rewrite(updated_rows)
        if (not success):
            return False, error, None
        else:
            return True, None, args.id

def delete(args):
    # Validate inputs
    if(not args.id or args.id <= 0):
        return False, err_code.ERR_INVALID_ID, None
    
    #Find matching row and delete
    success, error, rows = file_reader()
    if(not success):
        return False, error, None

    updated_rows = []
    found = False
    for row in rows:
        try:
            if int(row[expenseIdHeader]) == args.id:
                found = True
                continue
                
        except (ValueError, TypeError):
            return False, err_code.ERR_FILE_MALFORMED, None
    
        updated_rows.append(row)

    #Rewrite file is updated
    if not found:
        return False, err_code.ERR_ID_DNE, None
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
    count = 0
    if(args.month and (args.month <= 0 or args.month > 12)):
        return False, err_code.ERR_INVALID_MONTH, None

    success, error, rows = file_reader()
    if(not success):
        return False, error, None

    if(not args.month):
        for row in rows:
            try:
                count += Decimal(row[expenseAmountHeader])
            except (ValueError, TypeError):
                return False, err_code.ERR_FILE_MALFORMED, None
        return True, None, count
    else:
        try:
            for row in rows:
                if(datetime.strptime(row[expenseDateHeader], "%Y-%m-%d").month == args.month):
                    count += Decimal(row[expenseAmountHeader])
            return True, None, count
        except (ValueError, TypeError):
            return False, err_code.ERR_FILE_MALFORMED, None
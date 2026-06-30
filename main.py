import argparse
import expense_tracker as et
import calendar
import error_codes

def main(): 
    #Intialize argument parser
    parser = argparse.ArgumentParser(description="A simple expense tracker")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Input the the action to perform (add, update, delete, list, or summary)")

    # Define subcommands and bind them to their respective functions
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("--description", required=True, help="Input a description for the expense")
    parser_add.add_argument("--amount", required=True, type=float, help="Input the dollar amount of the expense")
    parser_add.add_argument("--date", help="Input the date of the expenditure in YYYY-MM-DD format")
    parser_add.set_defaults(func=et.add)

    parser_update = subparsers.add_parser("update")
    parser_update.add_argument("--id", required=True, type=int, help="Input the id of the expense to be update")
    parser_update.add_argument("--description", help="Input an updated description for the expense")
    parser_update.add_argument("--amount", type=float, help="Input the updated dollar amount of the expense")
    parser_update.set_defaults(func=et.update)

    parser_delete = subparsers.add_parser("delete")
    parser_delete.add_argument("--id",required=True, type=int, help="Input the id of the expense to be delete")
    parser_delete.set_defaults(func=et.delete)

    parser_list = subparsers.add_parser("list")
    parser_list.set_defaults(func=et.listExpenses)

    parser_summary = subparsers.add_parser("summary")
    parser_summary.add_argument("--month", type=int, help="Input the number of the month you want to see a summary of")
    parser_summary.set_defaults(func=et.summary)

    #Call respective function
    args = parser.parse_args()
    success, error, return_object = args.func(args)

    #Handle errors and print output
    if not success:
        print(error_codes.get_error_message(error))
    else:
        if args.command == "add":
            print(f"Expense added successfully (ID: {return_object})")
        elif args.command == "update":
            print(f"Expense updated successfully (ID: {return_object})")
        elif args.command == "delete":
            print(f"Expense deleted successfully (ID: {return_object})")
        elif args.command == "list":
            print(return_object.to_string())
        elif args.command == "summary" and not args.month:
            print(f"Total expenses: ${return_object}")
        elif args.command == "summary" and args.month:
            print(f"Total expenses for {calendar.month_name[args.month]}: ${return_object}")

        


if __name__ == "__main__":
    main()
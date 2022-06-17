# Imports used later in the code
import argparse
import csv
import time
from io import TextIOWrapper
from zipfile import ZipFile
import operator
import colorama
import datetime
import sys


arg_parser = argparse.ArgumentParser()
possible_actions = ['sort', 'search', 'filter', 'count']

# Set the script action
arg_parser.add_argument('action',
                        metavar='action',
                        type=str,
                        action='store',
                        choices=possible_actions,
                        help='sort = Sort by one of the columns of the CSV file.'
                             'search = Find all the occurrences of a term in'
                             ' the CSV file and highlight them in the terminal.'
                             'filter = keep only the rows that contain dates in a specified interval.'
                             'count = Count all the occurrences of a term in the CSV file and display the result.')

# Every action has a minimum of one argument
arg_parser.add_argument('action_param',
                        metavar='action_param',
                        type=str,
                        action='store',
                        help='Based on the chosen argument, you must add the specified parameter(s).')

# In order to actually use the filter action, we will need this
arg_parser.add_argument('--start_date', '-sd',
                        metavar='start_date',
                        type=str,
                        action='store',
                        help='if you use the filter function, this will be the lower bound '
                             'of the interval')

# This one too
arg_parser.add_argument('--end_date', '-ed',
                        metavar='end_date',
                        type=str,
                        action='store',
                        help='if you use the filter function, this will be the upper bound '
                             'of the interval')

# Optional limit argument
arg_parser.add_argument('--limit', '-lim',
                        nargs='?',
                        const=5,
                        type=int,
                        default=5,
                        action='store',
                        help='The number of rows that will be displayed after execution')

# Parse all the arguments
args = arg_parser.parse_args()

# Opening the csv file from the ZIP
with ZipFile('myFile0.zip') as zf:
    with zf.open('myFile0.csv', 'r') as data:
        reader = csv.reader(TextIOWrapper(data, 'utf-8'))
        # Keep the header, we might need it later
        header = next(reader)
        rows = []
        for row in reader:
            rows.append(row)

# Reformatting the employment date, to match the birthday
for i in range(len(rows)):
    rows[i][8] = datetime.datetime.strptime(rows[i][8], "%Y-%m-%d").strftime("%d-%m-%Y")

# Code for sorting the data
if args.action == 'sort':
    if args.action_param not in header:
        print("There is no column called " + args.action_param)
    else:
        # Sort by the header index of the item
        rows = sorted(rows, key=operator.itemgetter(header.index(args.action_param)))
        for i in range(0, args.limit):
            print(rows[i])

# Code for searching in the data
elif args.action == 'search':
    row_content = ''
    count_of_rows = 0
    colorama.init()
    for row in rows:
        if args.action_param in row:
            row_content = row_content + str(row) + '\n'
            count_of_rows += 1
        if count_of_rows is args.limit:
            break
    row_content = row_content.strip()
    # Highlight only the content of interest, like a CTRL+F
    row_content = row_content.replace(args.action_param,
                                      colorama.Fore.RED + args.action_param + colorama.Fore.RESET)
    print(row_content)

# Code for filtering the data
elif args.action == 'filter':
    if args.start_date is None and args.end_date is None:
        print(f'To filter the data, please provide the {colorama.Fore.RED}start date '
              f'{colorama.Fore.RESET}and {colorama.Fore.RED}end date{colorama.Fore.RESET}')
        sys.exit()
    result = []
    # Formatting the limits as dates
    lower_limit = time.strptime(args.start_date, "%d-%m-%Y")
    upper_limit = time.strptime(args.end_date, "%d-%m-%Y")
    for row in rows:
        current_iteration_date = time.strptime(row[header.index(args.action_param)], "%d-%m-%Y")
        # Checking if the date is in the desired interval. If it is, append the row to the result
        if lower_limit <= current_iteration_date <= upper_limit:
            result.append(row)
    # Maybe we don't have enough people to reach the args.limit
    max_len = min(args.limit, len(result))
    for i in range(max_len):
        print(result[i])

# Code for counting the number of occurrences of a string in the CSV
elif args.action == 'count':
    counter = 0
    for row in rows:
        counter += row.count(args.action_param)
    print(f'{str(counter)} occurrences of word {args.action_param} found in the CSV.')

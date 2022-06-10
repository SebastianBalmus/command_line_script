# Imports used later in the code
import argparse
import csv
import time
from io import TextIOWrapper
from zipfile import ZipFile
import operator
import colorama
import datetime

# No abbreviations will be allowed, due to the similarity of some words
arg_parser = argparse.ArgumentParser(allow_abbrev=False)

# Optional sort argument
arg_parser.add_argument('--sort', '-so',
                        metavar='column',
                        type=str,
                        action='store',
                        help='Sort by one of the columns of the CSV fie')

# Optional search argument
arg_parser.add_argument('--search', '-s',
                        metavar='term',
                        type=str,
                        action='store',
                        help='Find all the occurrences of a term in the CSV file and highlight them in the terminal')

# Optional filter argument
arg_parser.add_argument('--filter', '-f',
                        nargs=3,
                        metavar=('column', 'start_date', 'end_date'),
                        type=str,
                        action='store',
                        help='Only the ones that were born or employed in a period will be displayed')

# Optional count argument
arg_parser.add_argument('--count', '-c',
                        metavar='term',
                        type=str,
                        action='store',
                        help='Count all the occurrences of a term in the CSV file and display the result')

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
if args.sort is not None:
    if args.sort not in header:
        print("There is no column called " + args.sort)
    else:
        # Sort by the header index of the item
        rows = sorted(rows, key=operator.itemgetter(header.index(args.sort)))
        for i in range(0, args.limit):
            print(rows[i])

# Code for searching in the data
elif args.search is not None:
    print(args.search)
    row_content = ''
    colorama.init()
    # We don't want to append a useless newline at the end
    for i in range(0, args.limit):
        if i == args.limit - 1:
            row_content = row_content + (str(rows[i]))
        else:
            row_content = row_content + (str(rows[i])) + "\n"
    # Highlight only the content of interest, like a CTRL+F
    row_content = row_content.replace(args.search, colorama.Fore.RED + args.search + colorama.Fore.RESET)
    print(row_content)

# Code for filtering the data
elif args.filter is not None:
    result = []
    # Formatting the limits as dates
    lower_limit = time.strptime(args.filter[1], "%d-%m-%Y")
    upper_limit = time.strptime(args.filter[2], "%d-%m-%Y")
    for row in rows:
        current_iteration_date = time.strptime(row[header.index(args.filter[0])], "%d-%m-%Y")
        # Checking if the date is in the desired interval. If it is, append the row to the result
        if lower_limit <= current_iteration_date <= upper_limit:
            result.append(row)
    # Maybe we don't have enough people to reach the args.limit
    if len(result) < args.limit:
        max_len = len(result)
    else:
        max_len = args.limit
    for i in range(0, max_len):
        print(result[i])

# Code for counting the number of occurrences of a string in the CSV
elif args.count is not None:
    counter = 0
    for row in rows:
        counter += row.count(args.count)
    print(str(counter) + " occurrences of word" + args.count + " found in the CSV.")

# If we don't do anything with the script, a message must tell us what we can do to find out more
else:
    colorama.init()
    print("To see the functionality of this script, type " + colorama.Fore.RED + "\'py script.py -h\'" + colorama.Fore.RESET)

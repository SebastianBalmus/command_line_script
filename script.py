from ScriptClass import *


def main():
    # Get the arguments from the command line
    argument_list = Arguments().args

    # Read the data from the file
    data = ScriptData()
    data.read_data()

    # Get the method list of the ScriptActions class
    method_list = globals()['ScriptActions']

    # Call the required method according to the script arguments
    method = getattr(method_list, str(argument_list.action))
    method(argument_list, data.header, data.rows)


if __name__ == '__main__':
    main()

from script_class import *


def main():
    # Get the arguments from the command line
    argument_list = Arguments().args

    # Read the data from the file
    data = ScriptData()
    data.read_data()

    # Instantiate a ScriptActions object in order to use the class methods
    actions_object = ScriptActions()

    # Call the required method according to the script arguments
    action = getattr(actions_object, str(argument_list.action))
    action(argument_list, data.header, data.rows)


if __name__ == '__main__':
    main()

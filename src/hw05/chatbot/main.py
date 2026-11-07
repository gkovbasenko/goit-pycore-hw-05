from hw05.chatbot.data import parse_input
from hw05.chatbot.commands.add_contact import add_contact
from hw05.chatbot.commands.change_contact import change_contact
from hw05.chatbot.commands.show_phone import show_phone
from hw05.chatbot.commands.show_all import show_all

COMMANDS = [
    ("hello", "greet the bot"),
    ("add <name> <phone>", "add a new contact"),
    ("change <name> <phone>", "update an existing contact"),
    ("phone <name>", "show the phone number of a contact"),
    ("all", "list all contacts"),
    ("close | exit", "quit the assistant"),
]


def print_commands():
    width = max(len(usage) for usage, _ in COMMANDS)
    print("Available commands:")
    for usage, description in COMMANDS:
        print(f"  {usage.ljust(width)}  - {description}")


def main():
    contacts = {}

    print("Welcome to the assistant bot!")
    print_commands()
    while True:
        try:
            user_input = input("Enter a command: ")
        except (EOFError, KeyboardInterrupt):
            print("\nGood bye!")
            break

        command, *args = parse_input(user_input)

        if not command:
            print("Please enter a command.")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
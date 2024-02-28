from classes import AddressBook, Record


def input_error(func) -> callable:
    """Decorator function to handle input errors."""
    def inner(*args: list, **kwargs: dict):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Error: Key not found.'
        except ValueError:
            return 'Error: Invalid input format. Please provide the correct argument(s).'
        except IndexError:
            return 'Error: Insufficient arguments. Please provide the correct argument(s).'
        except Exception as e:
            return f'Error: {str(e)}. Please check your input and try again.'
    return inner

@input_error
def parse_input(user_input: str) -> tuple:
    """Parse user input."""
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args: tuple, book: AddressBook) -> str:
    """Add a new contact or update an existing contact's phone number."""
    name, phone = args
    record = book.find(name)

    if not record:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Contact added."

    record.add_phone(phone)
    return "Phone added"

@input_error
def change_contact(args: tuple, book: AddressBook) -> str:
    """Change an existing contact's phone number."""
    name, old_number, new_number = args
    record = book.find(name)

    if not record:
        return "Contact not found."

    record.edit_phone(old_number, new_number)
    return "Contact updated."

@input_error
def show_phone(args: tuple, book: AddressBook) -> str:
    """Show the phone number(s) of a contact."""
    name = args[0]
    record = book.find(name)

    if not record:
        return "Contact not found."

    return '; '.join(str(phone) for phone in record.phones)

@input_error
def add_birthday(args: tuple, book: AddressBook) -> str:
    """Add a birthday to a contact."""
    name, birthday = args
    record = book.find(name)
    
    if not record:
        return 'User does not exist.'
    
    record.add_birthday(birthday)
    return f"Birthday added."

@input_error
def show_birthday(args: tuple, book: AddressBook) -> str:
    """Show the birthday of a contact."""
    name = args[0]
    record = book.find(name)

    if not record:
        return "Contact not found."

    return record.birthday

@input_error
def show_all_birthdays(book: AddressBook) -> list:
    """Show upcoming birthdays within the next week."""
    return book.get_upcoming_birthdays()

def show_all(book: AddressBook) -> dict:
    """Show all contacts in the address book."""
    if not book:
        return "Book is empty."
    return book

commands_list = """
Commands:
1. add [name] [phone]: Add a new contact with a name and phone number, or update the phone number for an existing contact.
2. change [name] [new phone]: Change the phone number for the specified contact.
3. phone [name]: Show the phone number for the specified contact.
4. all: Show all contacts in the address book.
5. add-birthday [name] [date of birth]: Add the date of birth for the specified contact.
6. show-birthday [name]: Show the date of birth for the specified contact.
7. birthdays: Show upcoming birthdays within the next week.
8. hello: Receive a greeting from the bot.
9. close or exit: Close the program.
10. commands: Print the list of commands.
"""

def main() -> None:
    """Main function to run the address book application."""
    book = AddressBook()
    print("Welcome to the assistant bot!")
    print(commands_list)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ['close', 'quit', 'exit']:
            print("Goodbye!")
            break

        match command:
            case 'commands':
                print(commands_list)
            case 'hello':
                print("How can I help you?")
            case 'add':
                print(add_contact(args, book))
            case 'change':
                print(change_contact(args, book))
            case 'phone':
                print(show_phone(args, book))
            case 'add-birthday':
                print(add_birthday(args, book))
            case 'show-birthday':
                print(show_birthday(args, book))
            case 'birthdays':
                print(show_all_birthdays(book))
            case 'all':
                print(show_all(book))
            case _:
                print("Invalid command.")

if __name__ == '__main__':
    main()
from addressbook import AddressBook

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError as index_error:
            return index_error
        except ValueError as value_error:
            return value_error
        except KeyError as key_error:
            return key_error
        except AttributeError as attribute_error:
            return attribute_error
        except NotImplementedError:
            return "This feature is not implemented"
    return wrapper

def welcome_message(*args) -> str:  # noqa
    message = "Hi! How can i help you?"
    return message

def help_message(*args) -> str:  # noqa
    message = """
Commands and their usage:
add: 
    record 'name'                        : add name.
    phone 'name' 'phone'                 : add phone.
    email 'name' 'email'                 : add email.
    birthday 'name' 'birthday'           : add birthday (format yyyy-mm-dd).
change: 
    phone 'name' 'phone' 'new phone'     : change phone.
    email 'name' 'email'                 : change email. 
    birthday 'name' 'birthday'           : change birthday (format yyyy-mm-dd)
del: 
    record 'name'                        : delete contact.
    phone 'name' 'phone'                 : delete phone.
    email 'name' 'email'                 : delete email.
    birthday 'name' 'birthday'           : delete birthday.
    """
    return message

@input_error
def add_handler(ab: AddressBook, *args) -> str:
    if args[0] == 'record':
        ab.add_record(args[1])
        message = f'{args[1]} added to addressbook.'
    elif args[0] == 'phone':
        ab[args[1]].add_phone(args[2])
        message = f'Phone {args[2]} added to {args[1]}.'
    elif args[0] == 'email':
        ab[args[1]].set_email(args[2])
        message = f'Email {args[2]} added to {args[1]}.'
    elif args[0] == 'birthday':
        ab[args[1]].set_birthday(args[2])
        message = f'Birthday {args[2]} added to {args[1]}.'
    else:
        message = f'{args[0]}: wrong command.'
    return message

@input_error
def change_handler(ab: AddressBook, *args) -> str:
    if args[0] == 'phone':
        ab[args[1]].change_phone(args[2], args[3])
        message = f'Phone in {args[1]} was changed from {args[2]} to {args[3]} record.'
    elif args[0] == 'email':
        ab[args[1]].set_email(args[2])
        message = f'Email in {args[1]} was changed'
    elif args[0] == 'birthday':
        ab[args[1]].set_birthday(args[2])
        message = f'Birthday in {args[1]} was changed'
    else:
        message = f'{" ".join(args)}: wrong command.'
    return message

@input_error
def del_handler(ab: AddressBook, *args) -> str:
    if args[0] == 'record':
        ab.del_record(args[1])
        message = f'{args[1]} was deleted.'
    elif args[0] == 'phone':
        ab[args[1]].del_phone(args[2])
        message = f'Phone {args[2]} was deleted from {args[1]}.'
    elif args[0] == 'email':
        ab[args[1]].del_email()
        message = f'Email was deleted from {args[1]}.'
    elif args[0] == 'birthday':
        ab[args[1]].del_birthday()
        message = f'Birthday was deleted from {args[1]}.'
    else:
        message = f'del does not support {args[0]}.'
    return message

def show(ab: AddressBook, search='') -> str:
    table = ab.show(search)
    return table

def save_data(ab: AddressBook, *args) -> str:  # noqa
    ab.save_records_to_file('contacts.dat')
    return "Records have been saved."

def load_data(ab: AddressBook, *args) -> str:  # noqa
    ab.read_records_from_file('contacts.dat')
    return "Records have been loaded."

function = {'hello': welcome_message,
            'help': help_message,
            'add': add_handler,
            'change': change_handler,
            'del': del_handler,
            'show': show,
            'save': save_data,
            'load': load_data}

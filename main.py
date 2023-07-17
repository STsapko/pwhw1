from addressbook import AddressBook
from command_handlers import function

class Bot:
    @staticmethod
    def command_parser(ab: AddressBook, input_string) -> str:
        input_string = input_string.strip().lstrip()
        command = input_string.split()[0].lower()
        arguments = input_string.split()[1:]
        if command in function:
            message = function[command](ab, *arguments)
        elif input_string.lower() in ('good bye', 'exit', 'close', 'bye', '.'):
            message = '\nGood bye!\n'
        else:
            message = f'\n{command} is unknown!\n'
        return message

    def run(self):
        ab = AddressBook()
        try:
            print('\nType "help" for list of commands.\n')

            ab.read_records_from_file('contacts.dat')

            while True:
                input_string = input('Enter Command: ')

                if not len(input_string):
                    continue
                message = self.command_parser(ab, input_string)
                print(message)
                if message == '\nGood bye!\n':
                    break
        except Exception as e:
            print(f"Unexpected error occurred. {e}")

        finally:
            ab.save_records_to_file('contacts.dat')
            print("\nDon't worry. All saved")
            exit(0)  

def main() -> None:
    bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
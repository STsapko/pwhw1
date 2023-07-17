from abc import ABC, abstractmethod
from collections import UserDict
from prettytable import PrettyTable
import re
from datetime import date
import pickle

class Field(ABC):
    def __init__(self, value):
        self._value = None
        self.value = value
    
    @property    
    @abstractmethod
    def value(self):
        raise NotImplementedError
    
    @value.setter
    @abstractmethod
    def value(self, value):
        raise NotImplementedError
    
class Name(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        name_value_pattern = ''
        if re.match(name_value_pattern, value):
            self._value = value
        else:
            raise ValueError('Only letters')
        
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        if not re.compile(r'^(\d){1,20}$').match(value):
            raise ValueError("Phone number is not valid!")
        self._value = value
        
    def __eq__(self, _obj) -> bool:
        return self.value == _obj
    
class Email(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        if value.find('@') >= 0:
            self._value = value
        else:
            raise ValueError('@ is necessary')
        
    def __str__(self) -> str:
        return self._value
    
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
    
    @property
    def value(self) -> str:
        return self._value
    
    @value.setter
    def value(self, value) -> None:
        birthday_value_pattern = r"[-|_|\\|/]"
        d, m, y = map(int, re.split(birthday_value_pattern, value))
        birthday = date(y, m, d)
        if birthday <= date.today():
            self._value = birthday
        else:
            raise ValueError('Not in past')
        
    def __str__(self) -> str:
        return self._value.strftime('%Y-%m-%d')
    
class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        
    def add_phone(self, phone: str):
        phone = Phone(phone)
        if phone not in self.phones:
            self.phones.append(phone)
        else:
            raise ValueError(f"There is already {phone.value}")
        
    def change_phone(self, phone: str, new_phone: str):
        for phone in self.phones:
            if phone.value == phone:
                phone.value = new_phone
                break
            else:
                raise KeyError(f"There is no {phone}")
    
    def del_phone(self, phone: str):
        phone = Phone(phone)
        for phone in self.phones:
            if phone.value == phone:
                self.phones.remove(phone)
                break
            else:
                raise KeyError(f"There is no {phone}")
    
    def set_birthday(self, birthday: str):
        birthday = Birthday(birthday)
        self.birthday = birthday
        
    def del_birthday(self):
        self.birthday = None
        
    def set_email(self, email: str):
        self.email = Email(email)
        
    def del_email(self):
        self.email = None
        
    def days_to_birthday(self) -> int | None:
        if not self.birthday:
            return None
        today = date.today()
        try:
            birthday_this_year = self.birthday.value.replace(year=today.year)
        except ValueError:
            birthday_this_year = self.birthday.value.replace(year=today.year, day=today.day - 1)
        if birthday_this_year < today:
            birthday_this_year = self.birthday.value.replace(year=today.year + 1)
        days_to_birthday = (birthday_this_year - today).days
        return days_to_birthday
    
    def __str__(self):
        str_phones = "; ".join(phone.value for phone in self.phones)
        str_email = self.email.value if self.email else ""
        str_birthday = str(self.birthday) if self.birthday else ""
        return '|'.join((self.name.value, str_email, str_phones, str_birthday))
    
class AddressBook(UserDict):
    def add_record(self, name: str):
        if name not in self.data:
            self.data[name] = Record(name)
        else:
            raise KeyError(f'There is {name} already.')
        
    def del_record(self, name: str):
        if name in self.data:
            self.data.pop(name)
        else:
            raise KeyError(f"There is no {name}.")
        
    def get_all_records(self) -> list[Record]:
        records = []
        for record in self.data.values():
            records.append(record)
        return records
    
    def get_searched_records(self, search: str) -> list[Record]:
        records = []
        for record in self.data.values():
            if search in str(record):
                records.append(record)
        return records
    
    def show(self, search = '') -> str:
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Birthday", "Email"]
        for record in self.data.values():
            if search in str(record):
                name = record.name.value
                str_phones = "; ".join([phone.value for phone in record.phones]) if record.phones else "-"
                str_birthday = str(record.birthday) if record.birthday else "-"
                str_email = record.email.value if record.email else "-"
                table.add_row([name, str_phones, str_birthday, str_email])
        return str(table)
        
    def save_records_to_file(self, filename: str):
        with open(filename, "wb") as fw:
            pickle.dump(self.data, fw)

    def read_records_from_file(self, filename: str):
        try:
            with open(filename, "rb") as fr:
                content = pickle.load(fr)
                self.data.update(content)
        except FileNotFoundError:
            pass
        
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError(f'No {key}')
        
if __name__ == '__main__':
    ab = AddressBook()
    ab.read_records_from_file('contacts.dat')
    ab.add_record('A')
    ab['A'].add_phone('11')
    ab['A'].add_phone('22')
    ab['A'].add_phone('33')
    ab['A'].set_birthday('06-12-1979')
    ab['A'].set_email('a@a.com')
    ab['A'].del_phone('22')
    print(ab.show())
    
    
    
    
    
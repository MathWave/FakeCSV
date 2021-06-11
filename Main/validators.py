from random import choice, randrange


domains = ['com', 'ru', 'ua', 'net', 'org']


def string():
    letters = 'йцукенгшщзфывапролдячсмить'
    return ''.join([choice(letters) for _ in range(20)])


def en_string():
    letters = 'qwertyuiopasdfghjklzxcvbnm'
    return ''.join([choice(letters) for _ in range(20)])


class Validator:
    def create(self, *args):
        raise Exception('Method create should be implemented')


class AddressValidator(Validator):
    def create(self, *args):
        return f'ул. {string()}, д. {randrange(1, 20)}, кв. {randrange(1, 100)}'


class IntegerValidator(Validator):
    def create(self, *args):
        return randrange(*args)


class TextValidator(Validator):
    def create(self, *args):
        return '. '.join([' '.join([string() for _ in range(9)]) for _ in range(args[0])])


class CompanyValidator(Validator):
    def create(self, *args):
        company_types = ['ООО', 'ОАО', 'ЗАО', 'ИП']
        return f'{choice(company_types)} "{string()}"'


class PhoneValidator(Validator):
    def create(self, *args):
        return f'+7 (9{randrange(10, 100)}) {randrange(100, 1000)}-{randrange(10, 100)}-{randrange(10, 100)}'


class DomainValidator(Validator):
    def create(self, *args):
        return f'{en_string()}.{choice(domains)}'


class EmailValidator(Validator):
    def create(self, *args):
        return f'{en_string()}@{en_string()}.{choice(domains)}'


class FullnameValidator(Validator):
    def create(self, *args):
        return f'{string()} {string()}'

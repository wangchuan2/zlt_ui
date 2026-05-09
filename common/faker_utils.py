from faker import Faker


class FakerUtils:
    def __init__(self, locale="zh_CN"):
        self.faker = Faker(locale)

    def name(self):
        return self.faker.name()

    def phone(self):
        return self.faker.phone_number()

    def email(self):
        return self.faker.email()

    def address(self):
        return self.faker.address()

    def text(self, max_nb_chars=200):
        return self.faker.text(max_nb_chars=max_nb_chars)

    def company(self):
        return self.faker.company()

    def password(self, length=12):
        return self.faker.password(length=length)

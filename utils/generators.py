from faker import Faker
from config.data import ListingCategory, CreateListingData, UpdateListingData

fake = Faker("ru_RU")


class EmailGenerator:

    @staticmethod
    def generate():
        return fake.unique.email()


class PasswordGenerator:

    @staticmethod
    def generate():
        return fake.password(length=10)


class UserDataGenerator:

    @staticmethod
    def generate():
        email = EmailGenerator.generate()
        password = PasswordGenerator.generate()
        return email, password


class ListingDataGenerator:

    @staticmethod
    def create(category=ListingCategory.AUTO):
        return CreateListingData(
            name=fake.sentence(nb_words=4),
            category=category if isinstance(category, str) else category.value,
            description=fake.text(max_nb_chars=100),
            price=fake.random_int(min=100, max=100000),
            city=fake.city(),
        )

    @staticmethod
    def create_random():
        categories = [cat.value for cat in ListingCategory]
        category = fake.random_element(categories)
        return ListingDataGenerator.create(category)

    @staticmethod
    def update(name=None):
        return UpdateListingData(
            name=name or fake.sentence(nb_words=3),
            category=fake.random_element([cat.value for cat in ListingCategory]),
            description=fake.text(max_nb_chars=100),
            price=fake.random_int(min=100, max=100000),
            city=fake.city(),
        )

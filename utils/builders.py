from faker import Faker
from config.data import ListingCategory, ListingCondition, CreateListingData, UpdateListingData

fake = Faker("ru_RU")


class ListingDataBuilder:

    def __init__(self):
        self.name = ""
        self.category = ListingCategory.AUTO.value
        self.condition = ListingCondition.NEW.value
        self.city = "Москва"
        self.description = ""
        self.price = 0

    def with_name(self, name):
        self.name = name
        return self

    def with_category(self, category):
        self.category = category.value if isinstance(category, ListingCategory) else category
        return self

    def with_condition(self, condition):
        self.condition = condition.value if isinstance(condition, ListingCondition) else condition
        return self

    def with_city(self, city):
        self.city = city
        return self

    def with_description(self, description):
        self.description = description
        return self

    def with_price(self, price):
        self.price = price
        return self

    def build_create(self):
        return CreateListingData(
            name=self.name,
            category=self.category,
            condition=self.condition,
            city=self.city,
            description=self.description,
            price=self.price,
        )

    def build_update(self, name):
        return UpdateListingData(
            name=name,
            category=self.category,
            condition=self.condition,
            city=self.city,
            description=self.description,
            price=self.price,
        )

    @classmethod
    def default_create(cls):
        return cls().build_create()

    @classmethod
    def with_category_only(cls, category):
        return cls().with_category(category).build_create()

    @classmethod
    def random(cls):
        return cls().with_name(fake.sentence(nb_words=4)).with_category(
            fake.random_element([cat.value for cat in ListingCategory])
        ).with_price(fake.random_int(min=100, max=100000)).with_city(fake.city()).build_create()

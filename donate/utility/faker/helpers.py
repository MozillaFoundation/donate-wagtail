import factory
import random


# reseed the Faker RNG used by factory using seed
def reseed(seed):
    random.seed(seed)
    faker = factory.faker.Faker._get_faker(locale='en-US')
    faker.random.seed(seed)

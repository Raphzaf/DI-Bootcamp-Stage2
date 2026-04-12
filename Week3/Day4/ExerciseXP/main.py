import random
import string
from datetime import datetime


class Currency:
	def __init__(self, currency, amount):
		self.currency = currency
		self.amount = amount

	def __str__(self):
		label = self.currency if self.amount == 1 else f"{self.currency}s"
		return f"{self.amount} {label}"

	def __repr__(self):
		return str(self)

	def __int__(self):
		return self.amount

	def __add__(self, other):
		if isinstance(other, int):
			return self.amount + other

		if isinstance(other, Currency):
			if self.currency != other.currency:
				raise TypeError(
					f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
				)
			return self.amount + other.amount

		raise TypeError(
			f"Unsupported operand type(s) for +: 'Currency' and '{type(other).__name__}'"
		)

	def __iadd__(self, other):
		if isinstance(other, int):
			self.amount += other
			return self

		if isinstance(other, Currency):
			if self.currency != other.currency:
				raise TypeError(
					f"Cannot add between Currency type <{self.currency}> and <{other.currency}>"
				)
			self.amount += other.amount
			return self

		raise TypeError(
			f"Unsupported operand type(s) for +=: 'Currency' and '{type(other).__name__}'"
		)


def exercise_1_demo():
	print("=== Exercise 1: Currencies ===")
	c1 = Currency("dollar", 5)
	c2 = Currency("dollar", 10)
	c3 = Currency("shekel", 1)

	print(c1)
	print(int(c1))
	print(repr(c1))
	print(c1 + 5)
	print(c1 + c2)
	print(c1)

	c1 += 5
	print(c1)

	c1 += c2
	print(c1)

	try:
		print(c1 + c3)
	except TypeError as error:
		print(f"TypeError: {error}")


def random_string(length=5):
	letters = string.ascii_letters
	generated = ""
	for _ in range(length):
		generated += random.choice(letters)
	return generated


def show_current_date():
	today = datetime.now().date()
	print(f"Current date: {today}")


def time_until_new_year():
	now = datetime.now()
	next_year = datetime(year=now.year + 1, month=1, day=1)
	remaining = next_year - now
	print(f"Time left until January 1st: {remaining}")


def minutes_lived(birthdate_str, fmt="%Y-%m-%d"):
	birthdate = datetime.strptime(birthdate_str, fmt)
	now = datetime.now()
	total_minutes = int((now - birthdate).total_seconds() // 60)
	print(f"You have lived approximately {total_minutes:,} minutes.")


def generate_users(count):
	from faker import Faker

	fake = Faker()
	users = []
	for _ in range(count):
		users.append(
			{
				"name": fake.name(),
				"address": fake.address(),
				"language_code": fake.language_code(),
			}
		)
	return users


if __name__ == "__main__":
	exercise_1_demo()

	print("\n=== Exercise 3: Random String ===")
	print(random_string(5))

	print("\n=== Exercise 4: Current Date ===")
	show_current_date()

	print("\n=== Exercise 5: Time Until New Year ===")
	time_until_new_year()

	print("\n=== Exercise 6: Minutes Lived ===")
	minutes_lived("2000-01-01")

	print("\n=== Exercise 7: Faker Users ===")
	fake_users = generate_users(3)
	for user in fake_users:
		print(user)

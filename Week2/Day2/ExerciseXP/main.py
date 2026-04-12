import random


# Exercise 1: What Are You Learning?
def display_message():
    print("I am learning about functions in Python.")

display_message()


# Exercise 2: What's Your Favorite Book?
def favorite_book(title):
    print(f"One of my favorite books is {title}.")

favorite_book("Alice in Wonderland")


# Exercise 3: Some Geography
def describe_city(city, country="Unknown"):
    print(f"{city} is in {country}.")

describe_city("Reykjavik", "Iceland")
describe_city("Paris")


# Exercise 4: Random
def compare_numbers(number):
    random_number = random.randint(1, 100)
    if number == random_number:
        print("Success!")
    else:
        print(f"Fail! Your number: {number}, Random number: {random_number}")

compare_numbers(50)


# Exercise 5: Let's Create Some Personalized Shirts!
def make_shirt(size="large", text="I love Python"):
    print(f"The size of the shirt is {size} and the text is {text}.")

make_shirt()
make_shirt(size="medium")
make_shirt(size="small", text="Custom message")
make_shirt(size="small", text="Hello!")


# Exercise 6: Magicians
magician_names = ['Harry Houdini', 'David Blaine', 'Criss Angel']

def show_magicians(names):
    for name in names:
        print(name)

def make_great(names):
    for i in range(len(names)):
        names[i] = names[i] + " the Great"

make_great(magician_names)
show_magicians(magician_names)


# Exercise 7: Temperature Advice
def get_random_temp(season=None):
    if season == "winter":
        return round(random.uniform(-10, 5), 1)
    elif season == "spring":
        return round(random.uniform(8, 20), 1)
    elif season == "summer":
        return round(random.uniform(20, 40), 1)
    elif season == "autumn":
        return round(random.uniform(5, 15), 1)
    else:
        return round(random.uniform(-10, 40), 1)

def get_season_from_month(month):
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "autumn"

def main():
    month_input = input("Enter a month number (1-12) or press Enter to skip: ").strip()
    if month_input.isdigit() and 1 <= int(month_input) <= 12:
        season = get_season_from_month(int(month_input))
        print(f"Season: {season.capitalize()}")
        temp = get_random_temp(season)
    else:
        temp = get_random_temp()

    print(f"The temperature right now is {temp} degrees Celsius.")

    if temp < 0:
        print("Brrr, that's freezing! Wear some extra layers today.")
    elif temp < 16:
        print("Quite chilly! Don't forget your coat.")
    elif temp < 24:
        print("Nice weather.")
    elif temp <= 32:
        print("A bit warm, stay hydrated.")
    else:
        print("It's really hot! Stay cool.")

main()

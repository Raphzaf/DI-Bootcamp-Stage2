# Exercise 1
print("Hello world\n" * 4, end="")


# Exercise 2
print((99 ** 3) * 8)


# Exercise 3
snippets = [
    ("5 < 3", False),
    ("3 == 3", True),
    ('3 == "3"', False),
    ('"3" > 3', "TypeError"),
    ('"Hello" == "hello"', False),
]

for expression, guess in snippets:
    print(f"# Guess: {guess}")
    try:
        print(f">>> {expression} -> {eval(expression)}")
    except TypeError as error:
        print(f">>> {expression} -> {error.__class__.__name__}: {error}")


# Exercise 4
computer_brand = "Lenovo"

print(f"I have a {computer_brand} computer.")


# Exercise 5
name = "Rapha"
age = 25
shoe_size = 42
info = f"My name is {name}, I am {age} years old, my shoe size is {shoe_size}, and I enjoy learning Python."

print(info)


# Exercise 6
a = 20
b = 10

if a > b:
    print("Hello World")


# Exercise 7
number = int(input("Enter a number: "))

if number % 2 == 0:
    print("This number is even.")
else:
    print("This number is odd.")


# Exercise 8
my_name = "Rapha"
user_name = input("What is your name? ").strip()

if user_name.lower() == my_name.lower():
    print("We have the same name. The universe clearly copied its homework.")
else:
    print(f"Nice to meet you, {user_name}. My name is {my_name}, so we are officially different models.")


# Exercise 9
height = int(input("Enter your height in centimeters: "))

if height > 145:
    print("You are tall enough to ride.")
else:
    print("You need to grow some more to ride.")

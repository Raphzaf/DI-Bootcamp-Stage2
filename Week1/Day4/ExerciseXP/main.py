# ============================================================
# EXERCISE 1: Favorite Numbers (Sets)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 1: Favorite Numbers (Sets)")
print("="*60)

# Create a set with favorite numbers
my_fav_numbers = {3, 7, 11, 42, 13}
print(f"My favorite numbers: {my_fav_numbers}")

# Add two new numbers
my_fav_numbers.add(23)
my_fav_numbers.add(19)
print(f"After adding 23 and 19: {my_fav_numbers}")

# Remove the last number added (19)
my_fav_numbers.remove(19)
print(f"After removing 19: {my_fav_numbers}")

# Create friend's favorite numbers
friend_fav_numbers = {2, 5, 8, 23, 99}
print(f"Friend's favorite numbers: {friend_fav_numbers}")

# Concatenate sets using union
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print(f"Our combined favorite numbers: {our_fav_numbers}")
print(f"Note: Sets automatically remove duplicates (23 appears only once)")


# ============================================================
# EXERCISE 2: Tuple (Immutability)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 2: Tuple (Immutability)")
print("="*60)

# Create a tuple of integers
my_tuple = (1, 2, 3, 4, 5)
print(f"Original tuple: {my_tuple}")

# Try to add more integers to the tuple
print("\nAttempting to add integers to the tuple:")
try:
    my_tuple.append(6)
except AttributeError as e:
    print(f"Error: Tuples don't have an .append() method - {e}")

try:
    my_tuple[0] = 10
except TypeError as e:
    print(f"Error: Cannot modify tuple - {e}")

print("\nWhy? Tuples are IMMUTABLE - they cannot be changed after creation.")
print("If you need to add items, you must create a new tuple:")
new_tuple = my_tuple + (6, 7)
print(f"New tuple with added values: {new_tuple}")


# ============================================================
# EXERCISE 3: List Manipulation
# ============================================================
print("\n" + "="*60)
print("EXERCISE 3: List Manipulation")
print("="*60)

basket = ["Banana", "Apples", "Oranges", "Blueberries"]
print(f"Original basket: {basket}")

# Remove "Banana"
basket.remove("Banana")
print(f"After removing 'Banana': {basket}")

# Remove "Blueberries"
basket.remove("Blueberries")
print(f"After removing 'Blueberries': {basket}")

# Add "Kiwi" to the end
basket.append("Kiwi")
print(f"After appending 'Kiwi': {basket}")

# Add "Apples" to the beginning
basket.insert(0, "Apples")
print(f"After inserting 'Apples' at beginning: {basket}")

# Count how many times "Apples" appear
apples_count = basket.count("Apples")
print(f"'Apples' appears {apples_count} times in the basket")

# Empty the list
basket.clear()
print(f"After clearing the basket: {basket}")


# ============================================================
# EXERCISE 4: Floats (Generating Mixed Type Sequences)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 4: Floats (Mixed Type Sequences)")
print("="*60)

print("Question: What is a float? What's the difference from an integer?")
print("Answer: A float is a number with a decimal point.")
print("        Integer: 5 (no decimal) | Float: 5.0 (with decimal)")

print("\nGenerating sequence: 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5")
print("Method: Using loop to generate the sequence dynamically\n")

sequence = []
current = 1.5
while current <= 5:
    # Add integer if it's a whole number, otherwise add float
    if current == int(current):
        sequence.append(int(current))
    else:
        sequence.append(current)
    current += 0.5

print(f"Generated sequence: {sequence}")

# Alternative method using a more Pythonic approach
print("\nAlternative method:")
sequence_alt = []
for i in range(3, 11):  # 3 to 10 (inclusive)
    sequence_alt.append(i / 2)
print(f"Generated sequence: {sequence_alt}")


# ============================================================
# EXERCISE 5: For Loop (Range and Indexing)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 5: For Loop (Range and Indexing)")
print("="*60)

print("1. All numbers from 1 to 20 (inclusive):")
for num in range(1, 21):
    print(num, end=" ")
print("\n")

print("2. Every number from 1 to 20 where the index is even:")
for index in range(0, 20, 2):
    number = index + 1
    print(number, end=" ")
print("\n")


# ============================================================
# EXERCISE 6: While Loop (Input Validation)
# ============================================================
print("\n" + "="*60)
print("EXERCISE 6: While Loop (Input Validation)")
print("="*60)

print("Please enter your name (at least 3 letters, no digits):")

while True:
    name = input("Your name: ").strip()
    
    # Check if name has digits
    if name.isdigit():
        print("Invalid! Your name contains only digits. Please try again.")
        continue
    
    # Check if name is at least 3 characters long
    if len(name) < 3:
        print("Invalid! Your name must be at least 3 letters long. Please try again.")
        continue
    
    # Check if name contains any digits (mixed with letters)
    if any(char.isdigit() for char in name):
        print("Invalid! Your name contains digits. Please try again.")
        continue
    
    # Valid name
    print(f"Thank you, {name}!")
    break


# ============================================================
# EXERCISE 7: Favorite Fruits
# ============================================================
print("\n" + "="*60)
print("EXERCISE 7: Favorite Fruits")
print("="*60)

fruits_input = input("Enter your favorite fruits (separated by spaces): ").strip()
favorite_fruits = fruits_input.split()
print(f"Your favorite fruits: {favorite_fruits}")

test_fruit = input("Enter the name of any fruit: ").strip()

if test_fruit in favorite_fruits:
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")


# ============================================================
# EXERCISE 8: Pizza Toppings
# ============================================================
print("\n" + "="*60)
print("EXERCISE 8: Pizza Toppings")
print("="*60)

toppings = []
base_price = 10
topping_price = 2.50

print("Enter pizza toppings one by one. Type 'quit' to stop.\n")

while True:
    topping = input("Enter a topping (or 'quit' to finish): ").strip()
    
    if topping.lower() == 'quit':
        break
    
    if topping:  # Only add non-empty toppings
        toppings.append(topping)
        print(f"Adding {topping} to your pizza.")

print(f"\nYour pizza toppings: {toppings}")
total_cost = base_price + (len(toppings) * topping_price)
print(f"Base price: ${base_price:.2f}")
print(f"Toppings ({len(toppings)} x ${topping_price}): ${len(toppings) * topping_price:.2f}")
print(f"Total cost: ${total_cost:.2f}")


# ============================================================
# EXERCISE 9: Cinemax Tickets
# ============================================================
print("\n" + "="*60)
print("EXERCISE 9: Cinemax Tickets")
print("="*60)

print("Welcome to Cinemax!")
print("Ticket prices:")
print("  Free: Under 3 years old")
print("  $10: Ages 3-12")
print("  $15: Over 12 years old\n")

total_cost = 0
family_count = 0

while True:
    age_input = input("Enter the age of a family member (or 'done' to finish): ").strip()
    
    if age_input.lower() == 'done':
        break
    
    try:
        age = int(age_input)
        family_count += 1
        
        if age < 3:
            ticket_price = 0
            print(f"  Age {age}: Free")
        elif 3 <= age <= 12:
            ticket_price = 10
            print(f"  Age {age}: $10")
        else:
            ticket_price = 15
            print(f"  Age {age}: $15")
        
        total_cost += ticket_price
    except ValueError:
        print("Invalid input. Please enter a valid age.")

print(f"\nTotal family members: {family_count}")
print(f"Total ticket cost: ${total_cost:.2f}")


# ============================================================
# BONUS: Restricted Movie (Ages 16-21)
# ============================================================
print("\n" + "="*60)
print("BONUS: Restricted Movie (Ages 16-21)")
print("="*60)

print("This is a restricted movie (ages 16-21 only)\n")

attendees = []

while True:
    age_input = input("Enter the age of a person (or 'done' to finish): ").strip()
    
    if age_input.lower() == 'done':
        break
    
    try:
        age = int(age_input)
        
        if 16 <= age <= 21:
            attendees.append(age)
            print(f"  Age {age}: Allowed!")
        else:
            print(f"  Age {age}: Not allowed to watch this movie.")
    except ValueError:
        print("Invalid input. Please enter a valid age.")

print(f"\nFinal list of approved attendees: {attendees}")
print(f"Total attendees: {len(attendees)}")

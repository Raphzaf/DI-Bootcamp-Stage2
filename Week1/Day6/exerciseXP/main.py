# ============================================================================
# 🌟 EXERCISE 1: Converting Lists into Dictionaries
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 1: Converting Lists into Dictionaries")
print("="*70)

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

# Method 1: Using zip() function
result_dict_1 = dict(zip(keys, values))
print(f"\nMethod 1 (using zip): {result_dict_1}")

# Method 2: Using dictionary comprehension
result_dict_2 = {k: v for k, v in zip(keys, values)}
print(f"Method 2 (using dict comprehension): {result_dict_2}")

# Expected Output
print(f"\nExpected Output: {{'Ten': 10, 'Twenty': 20, 'Thirty': 30}}")


# ============================================================================
# 🌟 EXERCISE 2: Cinemax #2 - Movie Ticket Pricing
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 2: Cinemax - Movie Ticket Pricing")
print("="*70)

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}

def calculate_ticket_price(age):
    """Calculate ticket price based on age."""
    if age < 3:
        return 0  # Free
    elif 3 <= age <= 12:
        return 10  # $10
    else:
        return 15  # $15 (Over 12)

# Calculate total cost
total_cost = 0

print("\nTicket prices for each family member:")
for name, age in family.items():
    price = calculate_ticket_price(age)
    total_cost += price
    print(f"  {name.capitalize()}: {age} years old - ${price}")

print(f"\nTotal cost: ${total_cost}")

# BONUS: User input version
print("\n" + "-"*70)
print("BONUS: Calculate ticket cost for custom family")
print("-"*70)

def custom_family_ticket_cost():
    """Allow user to input family members and calculate total cost."""
    custom_family = {}
    print("\nEnter family members' names and ages (type 'done' to finish):")
    
    while True:
        name = input("Enter family member's name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        
        try:
            age = int(input(f"Enter {name}'s age: "))
            custom_family[name] = age
        except ValueError:
            print("Invalid input. Please enter a valid age.")
            continue
    
    if custom_family:
        total = 0
        print("\nTicket prices:")
        for name, age in custom_family.items():
            price = calculate_ticket_price(age)
            total += price
            print(f"  {name.capitalize()}: {age} years old - ${price}")
        print(f"\nTotal cost: ${total}")
    else:
        print("No family members entered.")

# Uncomment to run interactive bonus
# custom_family_ticket_cost()


# ============================================================================
# 🌟 EXERCISE 3: Zara Brand Dictionary
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 3: Zara Brand Dictionary")
print("="*70)

# Create the brand dictionary
brand = {
    "name": "Zara",
    "creation_date": 1975,
    "creator_name": "Amancio Ortega Gaona",
    "type_of_clothes": ["men", "women", "children", "home"],
    "international_competitors": ["Gap", "H&M", "Benetton"],
    "number_stores": 7000,
    "major_color": {
        "France": ["blue"],
        "Spain": ["red"],
        "US": ["pink", "green"]
    }
}

print("\nOriginal brand dictionary created.")

# Task 1: Change number_stores to 2
brand["number_stores"] = 2
print(f"\n1. Changed number_stores to: {brand['number_stores']}")

# Task 2: Print sentence describing Zara's clients
clothes_types = ", ".join(brand["type_of_clothes"])
print(f"\n2. Zara's clients: Zara serves {clothes_types} markets.")

# Task 3: Add new key country_creation
brand["country_creation"] = "Spain"
print(f"\n3. Added country_creation: {brand['country_creation']}")

# Task 4: Check if international_competitors exists and add "Desigual"
if "international_competitors" in brand:
    brand["international_competitors"].append("Desigual")
    print(f"\n4. Updated international_competitors: {brand['international_competitors']}")

# Task 5: Delete creation_date key
del brand["creation_date"]
print(f"\n5. Deleted creation_date key")

# Task 6: Print last item in international_competitors
last_competitor = brand["international_competitors"][-1]
print(f"\n6. Last international competitor: {last_competitor}")

# Task 7: Print major colors in US
us_colors = ", ".join(brand["major_color"]["US"])
print(f"\n7. Major colors in the US: {us_colors}")

# Task 8: Print number of keys
num_keys = len(brand)
print(f"\n8. Number of keys in brand dictionary: {num_keys}")

# Task 9: Print all keys
all_keys = list(brand.keys())
print(f"\n9. All keys in brand dictionary: {all_keys}")

# BONUS: Merge with another dictionary
print("\n" + "-"*70)
print("BONUS: Merge with more_on_zara dictionary")
print("-"*70)

more_on_zara = {
    "creation_date": 1975,
    "number_stores": 7000
}

# Create a copy to avoid modifying original
brand_copy = brand.copy()
brand_copy.update(more_on_zara)

print(f"\nOriginal brand keys: {list(brand.keys())}")
print(f"\nmore_on_zara: {more_on_zara}")
print(f"\nMerged dictionary keys: {list(brand_copy.keys())}")
print(f"\nMerged dictionary (sample): name={brand_copy['name']}, "
      f"creation_date={brand_copy['creation_date']}, "
      f"number_stores={brand_copy['number_stores']}")


# ============================================================================
# 🌟 EXERCISE 4: Disney Characters
# ============================================================================

print("\n" + "="*70)
print("EXERCISE 4: Disney Characters Dictionary Creation")
print("="*70)

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

# Dictionary 1: Character to Index
dict1 = {character: index for index, character in enumerate(users)}
print(f"\n1. Characters to Index:")
print(f"   {dict1}")

# Dictionary 2: Index to Character
dict2 = {index: character for index, character in enumerate(users)}
print(f"\n2. Index to Characters:")
print(f"   {dict2}")

# Dictionary 3: Sorted characters to Index
sorted_users = sorted(users)
dict3 = {character: index for index, character in enumerate(sorted_users)}
print(f"\n3. Sorted Characters to Index:")
print(f"   {dict3}")

print("\n" + "="*70)
print("✅ All exercises completed!")
print("="*70)

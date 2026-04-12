# Challenge 1: Letter Index Dictionary
word = input("Enter a word: ")
letter_indices = {}

for index, char in enumerate(word):
    if char in letter_indices:
        letter_indices[char].append(index)
    else:
        letter_indices[char] = [index]

print(letter_indices)


# Challenge 2: Affordable Items
items_purchase = {"Water": "$1", "Bread": "$3", "TV": "$1,000", "Fertilizer": "$20"}
wallet = "$300"

def clean_price(price_str):
    return int(price_str.replace("$", "").replace(",", ""))

budget = clean_price(wallet)
basket = []

for item, price_str in items_purchase.items():
    price = clean_price(price_str)
    if price <= budget:
        basket.append(item)
        budget -= price

if not basket:
    print("Nothing")
else:
    print(sorted(basket))

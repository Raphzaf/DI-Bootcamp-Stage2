# ============================================================
# Exercise 1: Cats
# ============================================================

class Cat:
    def __init__(self, cat_name, cat_age):
        self.name = cat_name
        self.age = cat_age


# Step 1: Create cat objects
cat1 = Cat("Whiskers", 3)
cat2 = Cat("Luna", 7)
cat3 = Cat("Mochi", 5)


# Step 2: Find the oldest cat
def find_oldest_cat(cat1, cat2, cat3):
    return max([cat1, cat2, cat3], key=lambda cat: cat.age)


# Step 3: Print the oldest cat's details
oldest = find_oldest_cat(cat1, cat2, cat3)
print(f"The oldest cat is {oldest.name}, and is {oldest.age} years old.")


# ============================================================
# Exercise 2: Dogs
# ============================================================

class Dog:
    def __init__(self, name, height):
        self.name = name
        self.height = height

    def bark(self):
        print(f"{self.name} goes woof!")

    def jump(self):
        print(f"{self.name} jumps {self.height * 2} cm high!")


# Step 2: Create dog objects
davids_dog = Dog("Rex", 50)
sarahs_dog = Dog("Bella", 35)

# Step 3: Print details and call methods
print(f"\n{davids_dog.name} is {davids_dog.height} cm tall.")
davids_dog.bark()
davids_dog.jump()

print(f"\n{sarahs_dog.name} is {sarahs_dog.height} cm tall.")
sarahs_dog.bark()
sarahs_dog.jump()

# Step 4: Compare dog sizes
print()
if davids_dog.height > sarahs_dog.height:
    print(f"{davids_dog.name} is the bigger dog.")
elif sarahs_dog.height > davids_dog.height:
    print(f"{sarahs_dog.name} is the bigger dog.")
else:
    print("Both dogs are the same size.")


# ============================================================
# Exercise 3: Who's the song producer?
# ============================================================

class Song:
    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)


stairway = Song([
    "There's a lady who's sure",
    "all that glitters is gold",
    "and she's buying a stairway to heaven"
])

print()
stairway.sing_me_a_song()


# ============================================================
# Exercise 4: Afternoon at the Zoo
# ============================================================

class Zoo:
    def __init__(self, zoo_name):
        self.name = zoo_name
        self.animals = []

    def add_animal(self, *args):
        for new_animal in args:
            if new_animal not in self.animals:
                self.animals.append(new_animal)

    def get_animals(self):
        print(f"Animals in {self.name}: {self.animals}")

    def sell_animal(self, animal_sold):
        if animal_sold in self.animals:
            self.animals.remove(animal_sold)

    def sort_animals(self):
        sorted_animals = sorted(self.animals)
        groups = {}
        for animal in sorted_animals:
            key = animal[0].upper()
            groups.setdefault(key, []).append(animal)
        return groups

    def get_groups(self):
        groups = self.sort_animals()
        for letter, animals in groups.items():
            print(f"{letter}: {animals}")


# Step 2: Create a Zoo instance
brooklyn_safari = Zoo("Brooklyn Safari")

# Step 3: Use the Zoo methods
print()
brooklyn_safari.add_animal("Giraffe", "Bear", "Baboon", "Cat", "Cougar", "Lion", "Zebra")
brooklyn_safari.get_animals()
brooklyn_safari.sell_animal("Bear")
brooklyn_safari.get_animals()
print()
brooklyn_safari.get_groups()

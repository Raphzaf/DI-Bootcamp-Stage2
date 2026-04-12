class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, **kwargs):
        for animal_type, count in kwargs.items():
            if animal_type in self.animals:
                self.animals[animal_type] += count
            else:
                self.animals[animal_type] = count

    def get_info(self):
        result = f"{self.name}'s farm\n\n"
        for animal, count in self.animals.items():
            result += f"{animal} : {count}\n"
        result += "\n    E-I-E-I-0!"
        return result

    def get_animal_types(self):
        return sorted(self.animals.keys())

    def get_short_info(self):
        animal_types = self.get_animal_types()
        animal_strings = [
            animal + "s" if self.animals[animal] > 1 else animal
            for animal in animal_types
        ]

        if len(animal_strings) == 1:
            animals_str = animal_strings[0]
        elif len(animal_strings) == 2:
            animals_str = f"{animal_strings[0]} and {animal_strings[1]}"
        else:
            animals_str = ", ".join(animal_strings[:-1]) + f" and {animal_strings[-1]}"

        return f"{self.name}'s farm has {animals_str}."


# Test the code
macdonald = Farm("McDonald")
macdonald.add_animal(cow=5)
macdonald.add_animal(sheep=1)
macdonald.add_animal(sheep=1)
macdonald.add_animal(goat=12)
print(macdonald.get_info())
print(macdonald.get_short_info())

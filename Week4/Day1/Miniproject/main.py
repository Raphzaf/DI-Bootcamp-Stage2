"""Week 4 - Day 1 - Mini Project

Part 1: Quiz answers
Part 2: Card and Deck classes
"""

from dataclasses import dataclass
import random


# Part 1: Quiz answers
QUIZ_ANSWERS = {
	"What is a class?": "A class is a blueprint for creating objects with shared attributes and methods.",
	"What is an instance?": "An instance is a concrete object created from a class.",
	"What is encapsulation?": "Encapsulation is bundling data and methods together and controlling direct access to internal state.",
	"What is abstraction?": "Abstraction is exposing only essential behavior while hiding implementation details.",
	"What is inheritance?": "Inheritance lets a class reuse and extend behavior from another class.",
	"What is multiple inheritance?": "Multiple inheritance is when a class inherits from more than one parent class.",
	"What is polymorphism?": "Polymorphism allows different classes to be used through the same interface, each with its own behavior.",
	"What is method resolution order or MRO?": "MRO is the order Python follows to find methods/attributes in inheritance chains.",
}


# Part 2: Deck of cards
@dataclass(frozen=True)
class Card:
	suit: str
	value: str

	def __str__(self) -> str:
		return f"{self.value} of {self.suit}"


class Deck:
	SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
	VALUES = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

	def __init__(self) -> None:
		self.cards: list[Card] = []
		self.shuffle()

	def shuffle(self) -> None:
		"""Reset deck to all 52 cards and shuffle them randomly."""
		self.cards = [Card(suit, value) for suit in self.SUITS for value in self.VALUES]
		random.shuffle(self.cards)

	def deal(self) -> Card:
		"""Deal one card from the deck and remove it."""
		if not self.cards:
			raise IndexError("No cards left in the deck. Shuffle to reset it.")
		return self.cards.pop()


if __name__ == "__main__":
	print("PART 1: QUIZ")
	for question, answer in QUIZ_ANSWERS.items():
		print(f"\nQ: {question}\nA: {answer}")

	print("\nPART 2: DECK DEMO")
	deck = Deck()
	print(f"Cards in new shuffled deck: {len(deck.cards)}")

	dealt_card = deck.deal()
	print(f"Dealt card: {dealt_card}")
	print(f"Cards remaining: {len(deck.cards)}")

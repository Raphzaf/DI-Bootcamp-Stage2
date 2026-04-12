import json
import random
from pathlib import Path


WORDS_FILE = Path(__file__).with_name("words.txt")
OUTPUT_JSON_FILE = Path(__file__).with_name("sample_json_output.json")


def get_words_from_file(file_path):
	"""Read words from a file and return them as a list."""
	with open(file_path, "r", encoding="utf-8") as file:
		content = file.read()

	words = content.split()
	return words


def get_random_sentence(sentence_length):
	"""Generate a random lowercase sentence with the given number of words."""
	words = get_words_from_file(WORDS_FILE)

	if not words:
		raise ValueError("The word list is empty.")

	random_words = [random.choice(words) for _ in range(sentence_length)]
	return " ".join(random_words).lower()


def run_json_exercise():
	"""Exercise 2: parse, modify, and save JSON data."""
	sample_json = """{
   "company":{
	  "employee":{
		 "name":"emma",
		 "payable":{
			"salary":7000,
			"bonus":800
		 }
	  }
   }
}"""

	data = json.loads(sample_json)

	salary = data["company"]["employee"]["payable"]["salary"]
	print(f"Salary: {salary}")

	data["company"]["employee"]["birth_date"] = "1998-04-12"

	with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as file:
		json.dump(data, file, indent=4)

	print(f"Modified JSON saved to: {OUTPUT_JSON_FILE}")


def main():
	print("This program generates a random sentence and runs a JSON exercise.")
	print("Random sentence length must be an integer between 2 and 20.")

	user_input = input("Enter desired sentence length (2-20): ")

	try:
		sentence_length = int(user_input)
		if sentence_length < 2 or sentence_length > 20:
			print("Error: Sentence length must be between 2 and 20.")
			return
	except ValueError:
		print("Error: Please enter a valid integer.")
		return

	try:
		sentence = get_random_sentence(sentence_length)
		print(f"Generated sentence: {sentence}")
	except FileNotFoundError:
		print(f"Error: Word file not found at {WORDS_FILE}")
		return
	except ValueError as error:
		print(f"Error: {error}")
		return

	print("\nRunning JSON exercise...")
	run_json_exercise()


if __name__ == "__main__":
	main()

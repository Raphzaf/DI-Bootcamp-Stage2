"""Daily challenge: text analysis and text cleaning with OOP."""

from __future__ import annotations

import re
import string


class Text:
	def __init__(self, text: str) -> None:
		self.text = text

	def _words(self) -> list[str]:
		"""Return a normalized list of words for analysis."""
		words = self.text.split()
		return [word.strip(string.punctuation).lower() for word in words if word.strip(string.punctuation)]

	def word_frequency(self, word: str) -> int | None:
		words = self._words()
		target = word.strip(string.punctuation).lower()
		count = words.count(target)
		return count if count > 0 else None

	def most_common_word(self) -> str | None:
		words = self._words()
		if not words:
			return None

		frequencies: dict[str, int] = {}
		for word in words:
			frequencies[word] = frequencies.get(word, 0) + 1

		return max(frequencies, key=frequencies.get)

	def unique_words(self) -> list[str]:
		words = self._words()
		# dict.fromkeys keeps insertion order and removes duplicates.
		return list(dict.fromkeys(words))

	@classmethod
	def from_file(cls, file_path: str) -> "Text":
		with open(file_path, "r", encoding="utf-8") as file:
			content = file.read()
		return cls(content)


class TextModification(Text):
	STOP_WORDS = {
		"a",
		"an",
		"and",
		"are",
		"as",
		"at",
		"be",
		"but",
		"by",
		"for",
		"if",
		"in",
		"into",
		"is",
		"it",
		"no",
		"not",
		"of",
		"on",
		"or",
		"such",
		"that",
		"the",
		"their",
		"then",
		"there",
		"these",
		"they",
		"this",
		"to",
		"was",
		"will",
		"with",
	}

	def remove_punctuation(self) -> str:
		translator = str.maketrans("", "", string.punctuation)
		self.text = self.text.translate(translator)
		return self.text

	def remove_stop_words(self) -> str:
		words = self.text.split()
		filtered_words = [word for word in words if word.lower() not in self.STOP_WORDS]
		self.text = " ".join(filtered_words)
		return self.text

	def remove_special_characters(self) -> str:
		# Keep letters, digits, and whitespace.
		self.text = re.sub(r"[^a-zA-Z0-9\s]", "", self.text)
		return self.text


if __name__ == "__main__":
	sample = "Hello world! Hello Python. This is a simple, simple test."

	text = Text(sample)
	print("Word frequency for 'simple':", text.word_frequency("simple"))
	print("Most common word:", text.most_common_word())
	print("Unique words:", text.unique_words())

	modified = TextModification(sample)
	print("Without punctuation:", modified.remove_punctuation())
	print("Without stop words:", modified.remove_stop_words())

	modified2 = TextModification("H@ello #World!! 123")
	print("Without special characters:", modified2.remove_special_characters())

from pathlib import Path


class AnagramChecker:
    def __init__(self, word_list_path: str | None = None) -> None:
        base_dir = Path(__file__).resolve().parent
        target_path = Path(word_list_path) if word_list_path else base_dir / "wordlist.txt"

        with open(target_path, "r", encoding="utf-8") as file:
            words = [word.strip().lower() for word in file.read().split()]

        self.words = [word for word in words if word.isalpha()]
        self.word_set = set(self.words)

    def is_valid_word(self, word: str) -> bool:
        normalized = word.strip().lower()
        return normalized in self.word_set

    @staticmethod
    def is_anagram(word1: str, word2: str) -> bool:
        normalized_word1 = word1.strip().lower()
        normalized_word2 = word2.strip().lower()

        if normalized_word1 == normalized_word2:
            return False

        return sorted(normalized_word1) == sorted(normalized_word2)

    def get_anagrams(self, word: str) -> list[str]:
        normalized = word.strip().lower()
        return [candidate for candidate in self.words if self.is_anagram(normalized, candidate)]

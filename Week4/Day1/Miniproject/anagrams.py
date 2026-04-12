from anagram_checker import AnagramChecker


def get_user_word() -> str | None:
    raw_input_word = input("Enter a word: ").strip()

    if len(raw_input_word.split()) != 1:
        print("Error: only one word is allowed.")
        return None

    if not raw_input_word.isalpha():
        print("Error: only alphabetic characters are allowed.")
        return None

    return raw_input_word.lower()


def show_results(checker: AnagramChecker, word: str) -> None:
    is_valid = checker.is_valid_word(word)
    anagrams = checker.get_anagrams(word)

    print(f"\nYOUR WORD: \"{word.upper()}\"")

    if is_valid:
        print("This is a valid English word.")
    else:
        print("This is NOT a valid English word.")

    if anagrams:
        print(f"Anagrams for your word: {', '.join(anagrams)}")
    else:
        print("No anagrams found.")


def main() -> None:
    checker = AnagramChecker()

    while True:
        print("\n=== Anagram Checker ===")
        print("1. Input a word")
        print("2. Exit")
        choice = input("Choose an option (1/2): ").strip()

        if choice == "2":
            print("Goodbye!")
            break

        if choice != "1":
            print("Invalid option. Please choose 1 or 2.")
            continue

        word = get_user_word()
        if word is None:
            continue

        show_results(checker, word)


if __name__ == "__main__":
    main()

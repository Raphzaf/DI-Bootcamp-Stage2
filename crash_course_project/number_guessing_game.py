"""Number guessing game (1 to 100) for beginners."""

import random


def play_game() -> None:
    """Run one game with a maximum of 7 attempts."""
    secret_number = random.randint(1, 100)
    max_attempts = 7

    print("Welcome to the number guessing game!")
    print("I am thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to find it.\n")

    for attempt in range(1, max_attempts + 1):
        while True:
            user_input = input(f"Attempt {attempt}/{max_attempts} - Enter a number: ")

            # Check that the input is a valid whole number.
            if user_input.isdigit():
                guess = int(user_input)
                break

            print("Invalid input. Please enter a whole number.")

        if guess == secret_number:
            print(f"Great job! You found the number in {attempt} attempt(s).")
            return

        if guess < secret_number:
            print("Too low!")
        else:
            print("Too high!")

        remaining_attempts = max_attempts - attempt
        if remaining_attempts > 0:
            print(f"You have {remaining_attempts} attempt(s) left.\n")

    print(f"Game over! The number was {secret_number}.")


if __name__ == "__main__":
    play_game()

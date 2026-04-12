# ============================================================================
# CHALLENGE 1: Multiples of a Number
# ============================================================================

def challenge_1_multiples():
    """Generate a list of multiples of a given number up to a specified length."""
    print("\n" + "="*50)
    print("CHALLENGE 1: Multiples of a Number")
    print("="*50)
    
    number = int(input("Enter a number: "))
    length = int(input("Enter the length (how many multiples): "))
    
    multiples = []
    for i in range(1, length + 1):
        multiples.append(number * i)
    
    print(f"Output: {multiples}")


# ============================================================================
# CHALLENGE 2: Remove Consecutive Duplicate Letters
# ============================================================================

def challenge_2_remove_duplicates():
    """Remove consecutive duplicate letters from a string."""
    print("\n" + "="*50)
    print("CHALLENGE 2: Remove Consecutive Duplicate Letters")
    print("="*50)
    
    word = input("Enter a word: ")
    
    result = ""
    for i, char in enumerate(word):
        # Add character if it's the first one or different from the previous
        if i == 0 or char != word[i - 1]:
            result += char
    
    print(f"Output: \"{result}\"")


# ============================================================================
# Main Menu
# ============================================================================

if __name__ == "__main__":
    while True:
        print("\n" + "="*50)
        print("Daily Challenge - Select an option:")
        print("="*50)
        print("1. Challenge 1: Multiples of a Number")
        print("2. Challenge 2: Remove Consecutive Duplicate Letters")
        print("3. Run Both Challenges")
        print("4. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            challenge_1_multiples()
        elif choice == "2":
            challenge_2_remove_duplicates()
        elif choice == "3":
            challenge_1_multiples()
            challenge_2_remove_duplicates()
        elif choice == "4":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

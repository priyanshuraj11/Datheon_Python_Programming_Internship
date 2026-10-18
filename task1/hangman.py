import random

WORDS = [
    "python", "computer", "programming", "developer",
    "keyboard", "hangman", "internet", "software",
    "database", "function", "variable", "algorithm",
    "education", "science", "technology", "student"
]

STAGES = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]


def play_game():
    word = random.choice(WORDS)
    guessed_letters = set()
    attempts = 6

    print("\nWelcome to Hangman!")
    print("Guess the hidden word one letter at a time.")
    print("You have 6 incorrect attempts.")

    while attempts > 0:
        print(STAGES[6 - attempts])

        display_word = " ".join(
            letter.upper() if letter in guessed_letters else "_"
            for letter in word
        )

        print("Word:", display_word)
        print("Guessed letters:", " ".join(
            sorted(letter.upper() for letter in guessed_letters)
        ) or "None")
        print("Attempts remaining:", attempts)

        if all(letter in guessed_letters for letter in word):
            print("\nCongratulations! You guessed the word:", word.upper())
            print("You win!")
            return

        guess = input("\nEnter a letter: ").strip().lower()

        if len(guess) != 1 or guess not in "abcdefghijklmnopqrstuvwxyz":
            print("Invalid input! Enter one English letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter. Try another.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print("Correct guess!")
        else:
            attempts -= 1
            print("Wrong guess!")

    print(STAGES[6])
    print("\nGame Over!")
    print("The correct word was:", word.upper())


def main():
    while True:
        play_game()

        choice = input("\nDo you want to play again? (yes/no): ").strip().lower()

        if choice not in ("yes", "y"):
            print("Thanks for playing Hangman!")
            break


if __name__ == "__main__":
    main()

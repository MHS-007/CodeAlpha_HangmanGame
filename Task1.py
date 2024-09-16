import random
import time
from nltk.corpus import words
import nltk
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Download the word list once
nltk.download('words')

# Use the word list from nltk
word_list = words.words()

# Choose difficulty levels
def choose_difficulty():
    print(Fore.CYAN + "\nChoose a difficulty level:")
    print("1. Easy (10 attempts, 60 seconds per round, 3 hints allowed)")
    print("2. Medium (6 attempts, 30 seconds per round, 2 hints allowed)")
    print("3. Hard (4 attempts, 15 seconds per round, 1 hint allowed)")
    choice = input("\nEnter the number corresponding to your choice: ").strip()

    if choice == '1':
        return 10, 60, 3
    elif choice == '2':
        return 6, 30, 2
    elif choice == '3':
        return 4, 15, 1
    else:
        print("Invalid choice! Defaulting to Medium difficulty.")
        return 6, 30, 2

# Select a random word
def select_random_word(word_list):
    return random.choice(word_list).upper()

# Display the current state of the word
def display_word(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

# Provide a hint by revealing a letter
def give_hint(word, guessed_letters):
    remaining_letters = [letter for letter in word if letter not in guessed_letters]
    if remaining_letters:
        hint_letter = random.choice(remaining_letters)
        print(Fore.YELLOW + f"Hint: The word contains the letter '{hint_letter}'.")
        return hint_letter
    return None

# Get a valid guess from the user with different colors for the prompt and input
def get_valid_guess():
    while True:
        print(Fore.BLUE + "\nGuess a letter (or type 'HINT' for a clue):", end=' ')
        guess = input(Fore.YELLOW).upper()  # Use a different color for the user's input
        
        if guess == "HINT":
            return guess
        elif len(guess) == 1 and guess.isalpha():
            return guess
        else:
            print(Fore.RED + "Invalid input. Please enter a single letter or type 'HINT'.")

# Main hangman game logic
def hangman():
    word = select_random_word(word_list)
    guessed_letters = set()
    attempts_left, time_limit, hints_left = choose_difficulty()
    score = 0

    # Decorative Welcome Message
    print()
    print(Fore.MAGENTA + "************************************")
    print(Fore.MAGENTA + "**                                **")
    print(Fore.MAGENTA + "**        Welcome to Hangman!     **")
    print(Fore.MAGENTA + "**                                **")
    print(Fore.MAGENTA + "************************************")
    print("\nYour word has been selected. Start guessing!\n")
    print(display_word(word, guessed_letters))

    start_time = time.time()

    while attempts_left > 0:
        # Check if the time limit has been exceeded
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            print(Fore.RED + f"\nTime's up! You had {int(elapsed_time)} seconds.")
            print(Fore.RED + "Game over! The word was " + Fore.YELLOW + f"'{word}'")
            break

        print(Fore.GREEN + f"\nTime remaining: {int(time_limit - elapsed_time)} seconds")
        print(Fore.CYAN + f"Hints remaining: {hints_left}")
        
        guess = get_valid_guess()

        if guess in guessed_letters:
            print(Fore.RED + f"You've already guessed the letter '{guess}'. Try again.")
        elif guess == "HINT":
            if hints_left > 0:
                hint_letter = give_hint(word, guessed_letters)
                guessed_letters.add(hint_letter)
                hints_left -= 1
                attempts_left -= 1
                print(f"Using a hint cost you 1 attempt. {attempts_left} attempts left.")
            else:
                print(Fore.RED + "No hints left!")
        elif guess in word:
            guessed_letters.add(guess)
            print(Fore.GREEN + "Good guess!")
        else:
            guessed_letters.add(guess)
            attempts_left -= 1
            print(Fore.RED + f"Wrong guess. You have {attempts_left} attempts left.")

        current_display = display_word(word, guessed_letters)
        print(current_display)

        if '_' not in current_display:
            print(Fore.CYAN + "\nCongratulations! You've guessed the word correctly.")
            score = attempts_left * 10 + int(time_limit - elapsed_time)
            print(Fore.CYAN + f"Your score is: {score}")
            break
    else:
        print(Fore.RED + "\nGame over! The word was " + Fore.YELLOW + f"'{word}'")

    return score

def main():
    total_score = 0
    while True:
        score = hangman()
        total_score += score
        print(Fore.YELLOW + f"Total score: {total_score}")
        play_again = input(Fore.CYAN + "\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again != 'yes':
            print(Fore.MAGENTA + "Thank you for playing Hangman! Goodbye.")
            break

if __name__ == "__main__":
    main()

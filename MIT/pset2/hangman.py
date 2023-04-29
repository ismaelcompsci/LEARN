# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
from doctest import FAIL_FAST
from operator import index
import random
import string

from zmq import Flag

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, "r")
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    # ITERATE OVER WORD
    for letter in secret_word:
        # IF LETTER FROM SECRET_WORD NOT IN LETTERS_GUESSED THE WORD IS NOT GUESSED
        if letter not in letters_guessed:
            return False
    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    word = ""

    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += "_"

    return word


def get_available_letters(letters_guessed):
    """
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"

    available_letters = ""

    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter

        else:
            continue

    return available_letters


def hangman(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    word = choose_word(load_words()).lower()

    unique_lets = len(set(word))

    guesses = 6
    warnings = 3

    letters_guessed = []

    vowel = ["a", "e", "i", "o", "u"]

    print("---------------------------Hangman--------------------------------")
    print(f"(+) The Word's length is {len(word)}")

    while True:
        if len(letters_guessed) == 0:
            pass
        else:
            print("---------------")

        if is_word_guessed(word, letters_guessed):
            print("(+) Congratulations, you won! ")
            print(f"Your total score is: {guesses * unique_lets}")
            break

        if guesses <= 0:
            print(f"(-) Sorry, you ran out of guesses. The word was {word}")
            break

        available_letters = get_available_letters(letters_guessed)
        print(f"(+) You have {guesses} guesses left")
        print(f"(+) You have {warnings} warnings left")
        print(f"(+) Available letters: {available_letters}")
        users_guess = input("(+) Please guess a letter: ").lower()

        if not str.isalpha(users_guess):
            if warnings <= 0:
                guesses -= 1
                print(
                    f"(-) Oops! That is not a valid letter. You have {guesses} guesses left: "
                )
                continue

            else:
                warnings -= 1
                print(
                    f"(-) Oops! That is not a valid letter. You have {warnings} warnings left: "
                )
                continue

        if users_guess in letters_guessed:
            if warnings <= 0:
                guesses -= 1
                print(
                    f"(-) Oops! You've already guessed that letter. You now have {guesses} guesses: {hangman_word}"
                )
                continue

            else:
                warnings -= 1
                print(
                    f"(-) Oops! You've already guessed that letter. You now have {warnings} warnings: {hangman_word}"
                )
                continue

        letters_guessed.append(users_guess)
        hangman_word = get_guessed_word(word, letters_guessed)

        if users_guess not in word:

            if users_guess in vowel:
                guesses -= 2
                print(f"(-) Oops! That letter is not in my word: {hangman_word}")
                continue

            print(f"(-) Oops! That letter is not in my word: {hangman_word}")
            guesses -= 1
            continue

        print(f"(*) Good Guess : {hangman_word}")


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------


def match_with_gaps(my_word, other_word):
    """
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    """
    my_word = my_word.replace(" ", "")
    no_white_space = len(my_word)

    # CHECK IF LENGTHS MATCH AFTER GETTING RID OF WHITESPACE
    if no_white_space != len(other_word):
        return False

    # make a guessed letters from my word ie: [a, p, l, e]
    # now check if the hidden letter is one of the letters

    missing_letter = []
    revealed_letters = []

    # my_word = my_word.strip()

    for i in range(len(my_word)):
        if my_word[i] == "_":
            missing_letter.append((other_word[i], i))
        else:
            revealed_letters.append(my_word[i])

    for letter, index in missing_letter:
        if my_word[int(index)] == "_" and letter in revealed_letters:
            return False

    return True


def show_possible_matches(my_word):
    """
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    # my_word = "t_ _ t"
    # print out all words in wordlist that match my_word
    # it should print no matches if there are no matches

    # my_word = my_word.replace(" ","")

    # guessed_letters = []

    # for letter in my_word:
    #     if letter != "_":
    #         guessed_letters.append(letter)

    possible_matches = []
    hits = []
    revealed_letters = []

    for word in wordlist:
        if match_with_gaps(my_word, word):

            possible_matches.append(word)

    WORD = my_word.replace(" ", "")
    for i in range(len(WORD)):
        if WORD[i] != "_":
            revealed_letters.append((WORD[i], i))

    add = True
    for word in possible_matches:
        for letter, index in revealed_letters:
            if word[index] != letter:
                add = False
                break
            add = True
        if add:
            hits.append(word)

    if not hits:
        print("No matches found")
        return

    return print(hits)


def hangman_with_hints(secret_word):
    """
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    """
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    word = choose_word(load_words()).lower()
    word = "apple"

    unique_lets = len(set(word))

    guesses = 6
    warnings = 3

    letters_guessed = []

    vowel = ["a", "e", "i", "o", "u"]

    print("---------------------------Hangman--------------------------------")
    print(f"(+) The Word's length is {len(word)}")

    while True:
        if len(letters_guessed) == 0:
            pass
        else:
            print("---------------")

        if is_word_guessed(word, letters_guessed):
            print("(+) Congratulations, you won! ")
            print(f"Your total score is: {guesses * unique_lets}")
            break

        if guesses <= 0:
            print(f"(-) Sorry, you ran out of guesses. The word was {word}")
            break

        available_letters = get_available_letters(letters_guessed)
        print(f"(+) You have {guesses} guesses left")
        print(f"(+) You have {warnings} warnings left")
        print(f"(+) Available letters: {available_letters}")
        users_guess = input("(+) Please guess a letter: ").lower()

        if not str.isalpha(users_guess) and not "*":
            if warnings <= 0:
                guesses -= 1
                print(
                    f"(-) Oops! That is not a valid letter. You have {guesses} guesses left: "
                )
                continue

            else:
                warnings -= 1
                print(
                    f"(-) Oops! That is not a valid letter. You have {warnings} warnings left: "
                )
                continue

        if users_guess in letters_guessed:
            if warnings <= 0:
                guesses -= 1
                print(
                    f"(-) Oops! You've already guessed that letter. You now have {guesses} guesses: {hangman_word}"
                )
                continue

            else:
                warnings -= 1
                print(
                    f"(-) Oops! You've already guessed that letter. You now have {warnings} warnings: {hangman_word}"
                )
                continue

        letters_guessed.append(users_guess)
        hangman_word = get_guessed_word(word, letters_guessed)

        if users_guess == "*":
            show_possible_matches(hangman_word)
            continue

        if users_guess not in word and not "*":

            if users_guess in vowel:
                guesses -= 2
                print(f"(-) Oops! That letter is not in my word: {hangman_word}")
                continue

            print(f"(-) Oops! That letter is not in my word: {hangman_word}")
            guesses -= 1
            continue

        print(f"(*) Good Guess : {hangman_word}")


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

    ###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

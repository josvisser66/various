#!/usr/bin/env python3

import random

# Take a sentence like "This is a test", remove the vowels, scramble
# shuffle the letter order of each word, and then remove the spaces.
# Given a dictionary of words, restore the sentence.

# I might/will not be possible to get the original sentence back because:
# - Words that consist of a single vowel (like "a") will disappear.
# - It is impossible to choose the right word if two words have the
#   same frequency representation with vowels removed (like "test" and "taste").

# We are using this mock dictionary instead of sourcing /usr/share/dict/words because
# /usr/share/dict/words comes with a ton of words that will make the examples
# less useful.
dictionary = set([
    "the",
    "this",
    "is",
    "ass",
    "an",
    "example",
    "axe",
    "sentence",
    "foo",
    "bar",
    "barrier",
    "shit",
    "test",
    "taste"
])
vowels = ["a", "e", "i", "o", "u"]


# Builds a frequency representation of a word (sorted, and without including the vowels).
# E.g. visser => r1s2v1
def frequency_representation(word):
    # Map of letter to frequency.
    freq = {}

    for letter in word:
        if letter in vowels:
            continue
        freq.setdefault(letter, 0)
        freq[letter] += 1

    result = ""

    for letter in sorted(freq.keys()):
        result += f"{letter}{freq[letter]}"

    return result


# Build reverse lookup from frequency representation to list of words in the dictionary
# for that representation.
rev = {}

for w in dictionary:
    f = frequency_representation(w)
    rev.setdefault(f, [])
    rev[f].append(w)


# Unscramble the sentence recursively.
# s is the scrambled sentence.
# sofar is a list of words (in frequency representation) that we have
# chosen so far. The last word is incomplete, meaning that we haven't
# figured out what that word is yet.
def unscramble(s, sofar):
    # While we have letters in s to process...
    while s:
        # Append the first letter of s to the last word in the solution so far.
        w = sofar.pop() + s[0]
        sofar.append(w)
        # And remove that letter from the scrambled string.
        s = s[1:]

        # If the last word in the solution so far unscrambles to a word, append it to the
        # solution so far and recurse from here.
        if frequency_representation(w) in rev:
            # We append an empty string to so far because we are going to try and add a
            # new word to the solution from whatever is in s.
            sofar.append("")
            solution = unscramble(s, sofar)

            # If we recursed into a solution we found one and we are done.
            if solution:
                return solution

            # When we get here the last word in sofar can be unscrambled, but
            # when we do that, we cannot unscramble the rest of the sentence.
            # Hence we should _not_ opt to unscramble the last word in sofar but
            # continue adding letters from s.
            # However at this point the last word of sofar contains all the
            # letters in the rest of s (because sofar is a list and was modified
            # by the recursive call to unscramble). We need to remove this
            # misguided attempt from sofar.
            # Note: This requires some understanding Python's implementation
            # of lists as references.
            sofar.pop()

    # When we get here, we have exhausted s. The question is whether there is
    # a solution in sofar or not. If the last word in sofar is empty then we have
    # a solution.
    if sofar[-1] == "":
        return sofar

    # Otherwise we have some stuff at the end which does not unscramble to a word
    # and we have no solution.
    return None


# Scramble a sentence according to the recipe given above.
def scramble(sentence):
    result = []

    for word in sentence.split(" "):
        new_word = []

        for letter in word:
            if letter not in vowels:
                new_word.append(letter)

        random.shuffle(new_word)
        result.extend(new_word)

    return "".join(result)


def main():
    original = "this is a test"
    scrambled = scramble(original)
    print("Original:", original)
    print("Scrambled:", scrambled)
    solution = unscramble(scrambled, [""])

    if not solution:
        print("No solution")
    else:
        # There is always an empty string at the end of this list.
        assert solution[-1] == ""
        solution.pop()
        # The reconstructed sentence with a guess for every possible word.
        guess0 = []
        # A full representation of the tree of possibilities.
        full = []

        for w in solution:
            possible = rev[frequency_representation(w)]
            guess0.append(possible[0])
            full.append('{' + w + ": " + ", ".join(possible) + '}')

        print("Unscrambled (first guess):", " ".join(guess0))
        print("Unscrambled (full tree):", " ".join(full))


if __name__ == "__main__":
    main()

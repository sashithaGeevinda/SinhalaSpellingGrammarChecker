
import re
from tqdm import tqdm
from Levenshtein import distance as levenshtein_distance

# Spellcheck main class
class SpellCheck:

    # Initialization method
    def __init__(self, word_dict_file=None):
        self.string_to_check = None

        # Open the dictionary file
        self.file = open(word_dict_file, 'r', encoding='utf-8')

        # Load the file data into a variable
        data = self.file.read()

        # Store all the words in a list
        data = data.split(",")

        # Change all the words to lowercase and remove duplicates
        data = [i.lower() for i in data]
        self.dictionary = list(set(data))

    def levenshtein_heuristic(self, word1, word2):
        """
        Calculates similarity score using Levenshtein Distance.
        The score is normalized between 0 and 100, where 100 indicates an exact match.
        """
        # Calculate Levenshtein distance
        distance = levenshtein_distance(word1, word2)

        # Normalize the score: 0 (completely different) to 100 (exact match)
        max_len = max(len(word1), len(word2))
        if max_len == 0:  # Avoid division by zero for empty strings
            return 100 if word1 == word2 else 0

        score = (1 - (distance / max_len)) * 100
        return score

    # String setter method
    def check(self, string_to_check):
        # Store the string to be checked in a class variable
        self.string_to_check = string_to_check

    # This method returns the possible suggestions of the correct words
    def suggestions(self):
        # Store the words of the string to be checked in a list by using a split function
        string_words = self.string_to_check.split()

        # A list to store all the possible suggestions
        suggestions = []

        # Loop over the number of words in the string to be checked
        for i in range(len(string_words)):
            best_match = None
            best_score = 0

            # Loop over words in the dictionary
            for name in self.dictionary:
                # Calculate the match score using Levenshtein heuristic
                score = self.levenshtein_heuristic(string_words[i].lower(), name.lower())

                # If the score is greater than the current best_score, update the best match
                if score >= 75 and score > best_score:
                    best_match = name
                    best_score = score

            # If a valid suggestion is found (best_match is not None), append it to the list
            if best_match:
                suggestions.append(best_match)

        # Return the suggestions list
        return suggestions

    # This method returns the corrected string of the given input
    def correct(self):
        # Use regex to split into words, punctuation, and whitespace, accounting for Unicode characters
        tokens = re.findall(r'\w+|[^\w\s]|\s+', self.string_to_check, re.UNICODE)

        # List to hold corrected tokens
        corrected_tokens = []

        for token in tqdm(tokens, "Correcting words: "):
            # Check if the token is a word (not punctuation or whitespace)
            if re.match(r'\w+', token, re.UNICODE):  # Match Unicode words
                best_match = None
                best_score = 0

                # Loop over the words in the dictionary
                for name in self.dictionary:
                    # Calculate the match probability using Levenshtein heuristic
                    score = self.levenshtein_heuristic(token.lower(), name.lower())

                    # If the score is greater than the current best_score and above the threshold
                    if score >= 75 and score > best_score:
                        best_match = name
                        best_score = score

                # If a valid best match is found, update the token
                if best_match:
                    corrected_tokens.append(best_match)
                else:
                    corrected_tokens.append(token)  # No match, keep the original word
            else:
                # If the token is not a word (punctuation or whitespace), keep it as is
                corrected_tokens.append(token)

        # Return the corrected string by joining the tokens
        corrected_string = "".join(corrected_tokens)

        return corrected_string

import re
from tqdm import tqdm


# spellcheck main class
class SpellCheck:

    # initialization method
    def __init__(self, word_dict_file=None):
        self.string_to_check = None

        # open the dictionary file
        self.file = open(word_dict_file, 'r', encoding='utf-8')

        # load the file data in a variable
        data = self.file.read()

        # store all the words in a list
        data = data.split(",")

        # change all the words to lowercase
        data = [i.lower() for i in data]

        # remove all the duplicates in the list
        data = set(data)

        # store all the words into a class variable dictionary
        self.dictionary = list(data)

    def letter_presence_score(self, word1, word2):
        letter_presence_score = 0

        sorted_word_1 = sorted(word1)
        sorted_word_2 = sorted(word2)

        i = 0
        j = 0

        while i < len(word1) and j < len(word2):
            if sorted_word_1[i] == sorted_word_2[j]:
                letter_presence_score += 1
                i += 1
                j += 1
            elif sorted_word_1[i] < sorted_word_2[j]:
                letter_presence_score -= 1
                i += 1
            elif sorted_word_1[i] > sorted_word_2[j]:
                letter_presence_score -= 1
                j += 1

        letter_presence_score -= max(len(word1) - i, len(word2) - j)

        return letter_presence_score

    def longest_common_substring_length(self, word1, word2):
        m, n = len(word1), len(word2)

        prev = [0] * (n + 1)
        curr = [0] * (n + 1)

        max_len = 0

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1] + 1
                    max_len = max(max_len, curr[j])
                else:
                    curr[j] = 0

            prev, curr = curr, prev

        return max_len

    def letter_arrangement_score(self, word1, word2):
        return self.longest_common_substring_length(word1, word2)

    def athulya_heuristic(self, word1, word2):
        """
        scoring should,
            - add score for each common letter
            - add score for correct arrangement
                - letters to the right, letters to the left
            - map from lowest possible score - highest possible score to 0 - 1
        :param word1: known word to compare
        :param word2: incorrect / reference word to compare
        :return: distance score
        """

        # max score when all letters are there, and they are in correct arrangement
        # max score = max_letter_presence_score + max_letter_arrangement_score
        max_score = 2 * len(word1)

        # min score = min letter presence score + min_letter_arrangement_score(0)
        min_score = -len(word1)

        letter_presence_score = self.letter_presence_score(word1, word2)

        letter_arrangement_score = 0
        if letter_presence_score != 0:
            letter_arrangement_score = self.letter_arrangement_score(word1, word2)

        total_score = letter_presence_score + letter_arrangement_score
        normalized_score = (total_score - min_score) / (max_score - min_score)

        return normalized_score * 100

    # string setter method
    def check(self, string_to_check):
        # store the string to be checked in a class variable
        self.string_to_check = string_to_check

    # this method returns the possible suggestions of the correct words
    def suggestions(self):
        # store the words of the string to be checked in a list by using a split function
        string_words = self.string_to_check.split()

        # a list to store all the possible suggestions
        suggestions = []

        # loop over the number of words in the string to be checked
        for i in range(len(string_words)):
            best_match = None
            best_score = 0

            # loop over words in the dictionary
            for name in self.dictionary:
                # calculate the match score using athulya_heuristic
                score = self.athulya_heuristic(string_words[i].lower(), name.lower())

                # if the score is greater than the current best_score, update the best match
                if score >= 50 and score > best_score:  # Lowered threshold for better flexibility
                    best_match = name
                    best_score = score

            # if a valid suggestion is found (best_match is not None), append it to the list
            if best_match:
                suggestions.append(best_match)

        # return the suggestions list
        return suggestions

    # this method returns the corrected string of the given input
    def correct(self):
        # Use regex to split into words, punctuation, and whitespace, accounting for Unicode characters
        # Updated regex to account for Sinhala characters as well
        tokens = re.findall(r'[\w\'\u0D80-\u0DFF]+|[^\w\s]|\s+', self.string_to_check, re.UNICODE)

        # List to hold corrected tokens
        corrected_tokens = []

        for token in tqdm(tokens, "Correcting words: "):
            # Check if the token is a word (not punctuation or whitespace)
            if re.match(r'[\w\'\u0D80-\u0DFF]+', token, re.UNICODE):  # Match Sinhala and other Unicode words
                best_match = None
                best_score = 0

                # Loop over the words in the dictionary
                for name in self.dictionary:
                    # Calculate the match probability using athulya_heuristic
                    score = self.athulya_heuristic(token.lower(), name.lower())

                    # If the score is greater than the current best_score and above the threshold
                    if score >= 70 and score > best_score:  # Lowered threshold for better flexibility
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

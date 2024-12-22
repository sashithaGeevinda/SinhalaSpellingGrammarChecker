from .POSTagger_HMC import POSTagger, load_data
from tqdm import tqdm


class GrammarChecker:
    def __init__(self, pos_tagger_dataset_location: str):
        self.sentences, self.tags = load_data(pos_tagger_dataset_location)

        self.pos_tagger = POSTagger()
        self.pos_tagger.train(self.sentences, self.tags)

    def check_grammar(self, paragraph):
        """
        Checks grammar rules for a given paragraph and returns letter index ranges for erroneous sentences.

        Args:
            paragraph (str): The input paragraph to check.

        Returns:
            List[Tuple[int, int]]: A list of tuples with the start and end character indices of erroneous sentences.
        """
        # Split the paragraph into sentences, keeping track of their start and end indices
        sentences = paragraph.split(".")  # Use Sinhala sentence-ending marker
        start_indices = []
        current_index = 0

        for sentence in sentences:
            start_indices.append(current_index)
            current_index += len(sentence) + 1  # +1 for the sentence-ending marker

        erroneous_ranges = []

        for i, sentence in tqdm(enumerate(sentences), desc="Detecting Erroneous Sentences: ", total=len(sentences)):
            # Ignore empty sentences
            if not sentence.strip():
                continue

            # Get the start and end indices of the current sentence in the paragraph
            start_index = start_indices[i]
            end_index = start_index + len(sentence)

            # Tokenize the sentence into words
            words = sentence.split()

            # Get POS tags for the sentence using the pos_tagger
            pos_tags = self.pos_tagger.predict(words)
            # print(pos_tags)

            # Check for grammar rules in the sentence
            for j, word in enumerate(words):
                # Rule 1: 'මම' followed by a 'VFM' word should end with 'මි'
                if word == "මම":
                    for k in range(j + 1, len(words)):  # Look at all words after 'මම'
                        if pos_tags[k] == "VFM" or pos_tags[k] == "VP":  # Check if the POS tag is 'VFM'
                            if not words[k].endswith("මි"):
                                erroneous_ranges.append((start_index, end_index))
                                break
                    else:
                        continue  # No match found; move to next word
                    break  # Match found; exit the outer loop

                # Rule 2: 'අපි' followed by a 'VFM' word should end with 'මු'
                if word == "අපි":
                    for k in range(j + 1, len(words)):  # Look at all words after 'අපි'
                        if pos_tags[k] == "VFM" or pos_tags[k] == "VP":  # Check if the POS tag is 'VFM'
                            if not words[k].endswith("මු"):
                                erroneous_ranges.append((start_index, end_index))
                                break
                    else:
                        continue  # No match found; move to next word
                    break  # Match found; exit the outer loop

        return erroneous_ranges


# Initialize the GrammarChecker with the POS tagger
if __name__ == "__main__":
    grammar_checker = GrammarChecker(pos_tagger_dataset_location="POSTagDataset/tagged_sentences.txt")

    # Input paragraph
    paragraph = ("මම ඊයේ උද්‍යානයට ගියා, ළමයි ටිකක් පැසිපන්දු ක්‍රීඩා කරනවා දැක්කා. මමයි මල්ලියි එයාලට සෙල්ලමකට එකතු "
                 "වුණා. අපි එහෙට මෙහෙට දුවලා හිනාවෙලා හරිම විනෝදයෙන් හිටියා. පසුව ඔවුන්ගෙන් එක් අයෙක් අපට ඔවුන්ගේ "
                 "නිවසට කෙටි ආහාර සඳහා ආරාධනා කළේය. එදා අලුත් යාලුවො ගැන මට ලොකු සතුටක් දැනුනා.")

    # Run the grammar checker
    erroneous_char_ranges = grammar_checker.check_grammar(paragraph)

    # Output erroneous letter index ranges
    print("Erroneous letter index ranges:", erroneous_char_ranges)

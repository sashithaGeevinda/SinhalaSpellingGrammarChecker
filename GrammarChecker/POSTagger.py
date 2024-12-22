from collections import defaultdict, Counter
from tqdm import tqdm
import re


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    sentences, tags = [], []
    sentence, tag_seq = [], []

    i = 0
    while i < len(lines):
        line = lines[i]
        try:
            if line.strip():
                word, tag = line.split()
                # Clean the tag to include only English letters and capitalize them
                tag = ''.join(re.findall(r'[a-zA-Z]', tag)).upper()
                sentence.append(word)
                tag_seq.append(tag)

                # Check for full stop (FS) to mark the end of a sentence
                if tag == 'FS':
                    sentences.append(sentence)
                    tags.append(tag_seq)
                    sentence, tag_seq = [], []
        except Exception as e:
            print(f"Error processing line: {line}")
            print(e)
            # Skip to the next full stop (FS)
            while i < len(lines):
                i += 1
                if lines[i].strip():
                    try:
                        _, tag = lines[i].split()
                        tag = ''.join(re.findall(r'[a-zA-Z]', tag)).upper()
                        if tag == 'FS':
                            break
                    except Exception:
                        continue
            sentence, tag_seq = [], []  # Reset sentence and tags
        finally:
            i += 1

    # Add the last sentence if not added
    if sentence:
        sentences.append(sentence)
        tags.append(tag_seq)

    return sentences, tags


class POS_Tagger:
    def __init__(self, file_path):
        """
        Initializes the POS tagger with a dataset loaded from a file.
        file_path: Path to the file containing tagged sentences.
        """
        self.constant_tags = {}  # Dictionary for words with constant POS tags
        self.ambiguous_words = defaultdict(Counter)  # Dictionary for words with multiple POS tags
        self.context_rules = defaultdict(Counter)  # Rules based on neighboring POS patterns
        sentences, tags = load_data(file_path)
        tagged_sentences = list(zip(sentences, tags))
        self._train(tagged_sentences)

    def _train(self, tagged_sentences):
        """
        Trains the tagger by analyzing the tagged sentences.
        """
        word_tag_counts = defaultdict(Counter)

        for words, tags in tqdm(tagged_sentences, desc="Processing Sentences", leave=False):
            for i, (word, tag) in enumerate(zip(words, tags)):
                word_tag_counts[word][tag] += 1

                # Create context rules for ambiguous words
                if len(tags) > 1:
                    left_context = tags[i - 1] if i > 0 else None
                    right_context = tags[i + 1] if i < len(tags) - 1 else None
                    context = (left_context, right_context)
                    self.context_rules[(word, context)][tag] += 1

        # Separate constant tags from ambiguous ones
        for word, tag_count in tqdm(word_tag_counts.items(), desc="Classifying Words", leave=True):
            if len(tag_count) == 1:
                self.constant_tags[word] = next(iter(tag_count))
            else:
                self.ambiguous_words[word] = tag_count

    def _get_best_tag(self, word, left_tag, right_tag):
        """
        Determines the best POS tag for a word based on context.
        """
        context = (left_tag, right_tag)
        if (word, context) in self.context_rules:
            return self.context_rules[(word, context)].most_common(1)[0][0]
        # Default to most frequent tag if context match fails
        if word in self.ambiguous_words and self.ambiguous_words[word]:
            return self.ambiguous_words[word].most_common(1)[0][0]
        # Fallback for unknown words
        return "UNK"

    def tag_sentence(self, sentence):
        """
        Tags a sentence using the trained POS tagger.
        sentence: List of words to tag.
        Returns: List of predicted POS tags.
        """
        tags = [None] * len(sentence)

        # Tag words with constant tags
        for i, word in tqdm(enumerate(sentence), desc="Tagging Constant Words", leave=False):
            if word in self.constant_tags:
                tags[i] = self.constant_tags[word]

        # Tag ambiguous words using context
        for i, word in tqdm(enumerate(sentence), desc="Resolving Ambiguous Words", leave=True):
            if tags[i] is None:  # Only process untagged words
                left_tag = tags[i - 1] if i > 0 else None
                right_tag = tags[i + 1] if i < len(sentence) - 1 else None
                tags[i] = self._get_best_tag(word, left_tag, right_tag)

        return tags


# Example usage
if __name__ == "__main__":
    file_path = "POSTagDataset/tagged_sentences.txt"  # Replace with the path to your data file
    pos_tagger = POS_Tagger(file_path)
    test_sentence = ["ඊශ්‍රායල්", "මිසයිල", "ප්‍රහාර", "වලින්", "පලස්තීනුවෝ", "4", "ක්", "මිය", "යති"]
    print(pos_tagger.tag_sentence(test_sentence))

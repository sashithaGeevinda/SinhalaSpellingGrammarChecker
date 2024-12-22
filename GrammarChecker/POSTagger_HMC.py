import re
from collections import defaultdict, Counter
import math
from tokenizers import ByteLevelBPETokenizer


class POSTagger:
    def __init__(self):
        self.transition_probs = defaultdict(lambda: defaultdict(float))
        self.emission_probs = defaultdict(lambda: defaultdict(float))
        self.tags = set()
        self.vocab = set()
        self.tokenizer = ByteLevelBPETokenizer()

    def train_tokenizer(self, sentences):
        """Train the byte-pair tokenizer on the given corpus."""
        with open("temp_corpus.txt", "w", encoding="utf-8") as f:
            for sentence in sentences:
                f.write(" ".join(sentence) + "\n")

        self.tokenizer.train(["temp_corpus.txt"], vocab_size=30000, min_frequency=2)

    def train(self, sentences, tags):
        """
        Train the HMM-based POS tagger.
        :param sentences: List of sentences (list of words).
        :param tags: List of corresponding POS tag sequences.
        """
        self.train_tokenizer(sentences)

        tag_bigrams = Counter()
        word_tag_pairs = Counter()
        tag_counts = Counter()

        for sentence, tag_seq in zip(sentences, tags):
            for i, (word, tag) in enumerate(zip(sentence, tag_seq)):
                self.vocab.add(word)
                self.tags.add(tag)
                word_tag_pairs[(word, tag)] += 1
                tag_counts[tag] += 1

                if i > 0:
                    prev_tag = tag_seq[i - 1]
                    tag_bigrams[(prev_tag, tag)] += 1

        # Calculate transition probabilities
        for (prev_tag, curr_tag), count in tag_bigrams.items():
            self.transition_probs[prev_tag][curr_tag] = count / tag_counts[prev_tag]

        # Calculate emission probabilities
        for (word, tag), count in word_tag_pairs.items():
            self.emission_probs[tag][word] = count / tag_counts[tag]

        # Add smoothing for unseen transitions
        for tag in self.tags:
            for next_tag in self.tags:
                if next_tag not in self.transition_probs[tag]:
                    self.transition_probs[tag][next_tag] = 1e-6

    def predict(self, sentence):
        """
        Predict the POS tags for a given sentence using the Viterbi algorithm.
        :param sentence: List of words.
        :return: List of predicted POS tags and their confidence levels.
        """
        n = len(sentence)
        viterbi = defaultdict(lambda: defaultdict(lambda: -math.inf))
        backpointer = defaultdict(lambda: defaultdict(str))

        # Initialization
        for tag in self.tags:
            word = sentence[0]
            emission = self._get_emission_prob(word, tag)
            viterbi[0][tag] = math.log(self.transition_probs['START'][tag] + 1e-6) + math.log(emission)

        # Recursion
        for i in range(1, n):
            for curr_tag in self.tags:
                for prev_tag in self.tags:
                    prob = (
                        viterbi[i - 1][prev_tag]
                        + math.log(self.transition_probs[prev_tag][curr_tag] + 1e-6)
                        + math.log(self._get_emission_prob(sentence[i], curr_tag))
                    )
                    if prob > viterbi[i][curr_tag]:
                        viterbi[i][curr_tag] = prob
                        backpointer[i][curr_tag] = prev_tag

        # Termination
        best_tag = None
        best_prob = -math.inf
        for tag in self.tags:
            prob = viterbi[n - 1][tag]
            if prob > best_prob:
                best_prob = prob
                best_tag = tag

        # Backtrace
        predicted_tags = [best_tag]
        for i in range(n - 1, 0, -1):
            best_tag = backpointer[i][best_tag]
            predicted_tags.insert(0, best_tag)

        # Normalize confidences to a scale of 0-1 based on the max score in the Viterbi path
        max_score = max(max(viterbi[i].values()) for i in range(n))

        return predicted_tags

    def _get_emission_prob(self, word, tag):
        """
        Get the emission probability for a word and a tag. If the word is unknown,
        use byte-pair tokenization to estimate its probability.
        """
        if word in self.emission_probs[tag]:
            return self.emission_probs[tag][word]

        # Byte-pair tokenization for unknown words
        subwords = self.tokenizer.encode(word).tokens
        prob = 1e-6
        for subword in subwords:
            if subword in self.vocab:
                prob += 1e-3
        return prob


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
            # print(f"Error processing line: {line}")
            # print(e)
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


if __name__ == "__main__":
    # Example Usage
    file_path = "POSTagDataset/tagged_sentences.txt"
    sentences, tags = load_data(file_path)

    pos_tagger = POSTagger()
    pos_tagger.train(sentences, tags)

    # Test with a new sentence
    test_sentence = ["ඊශ්‍රායල්", "මිසයිල", "ප්‍රහාර", "වලින්", "පලස්තීනුවෝ", "4", "ක්", "මිය", "යති"]
    predicted_tags = pos_tagger.predict(test_sentence)
    print(test_sentence, predicted_tags)

    test_sentence = ["මගේ", "නම", "ඛාන්", "සහ", "මගේ", "සහෝදරයන්", "4", "දෙනා", "බාන්"]
    predicted_tags = pos_tagger.predict(test_sentence)
    print(test_sentence, predicted_tags)

    test_sentence = ["මම", "උදේට", "බත්", "කරමු"]
    predicted_tags = pos_tagger.predict(test_sentence)
    print(test_sentence, predicted_tags)

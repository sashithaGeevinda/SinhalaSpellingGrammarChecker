from GrammarChecker.GrammarChecker import GrammarChecker as gc
from GrammarChecker.RAGGrammarCorrect import GrammarCorrector as corrector
from SpellChecker.SpellCheckerByLevenshteinEditDistance import SpellCheck as sc


class GrammarSpellChecker:
    def __init__(self, spelling_dict, POS_dataset):
        self.spell_checker = sc(spelling_dict)
        self.grammar_checker = gc(POS_dataset)

    def correct_spelling(self, paragraph):
        self.spell_checker.check(paragraph)
        return self.spell_checker.correct()

    def detect_grammar_errors(self, paragraph):
        return self.grammar_checker.check_grammar(paragraph)


if __name__ == "__main__":
    paragraphs = [
        "මම අද රෑ කෑබට සිල්ලර බඩු ටිකක් ගන්න කඩේට ගියා.",
        "මම විරද්‍යාව හා තාක්ෂකය ගැන පොත් කියවන්න කැමතියි.",
        "අපි ඊයේ වෙරළ තීරයේ හිරු බැස් යෑම නැරඹීමෙන් සතුටක් ලැබුවා.",
        "අපි ගෙවත්තේ අලුත් මල් සිටුවා එය දීප්තිමමත් කරන්න.",
        "අපි එකට ෆිල්ම් එකක් බලාලා හොඳට විනෝද වුණා.",
        "මම අවසාන විභාගරයට සූදානම් වෙන්නන පැය ගගණන් පාඩකම් කළා."
    ]

    # Initialize spelling and grammar checker
    gsc = GrammarSpellChecker("SpellChecker/corrected_sinhala_words.txt", "GrammarChecker/POSTagDataset/tagged_sentences.txt")

    # Correct spelling errors
    corrected_paragraphs = [gsc.correct_spelling(paragraph) for paragraph in paragraphs]
    # corrected_paragraphs = paragraphs

    # Detect grammar errors
    grammar_errors = []
    for idx, paragraph in enumerate(corrected_paragraphs):
        error_indices = gsc.detect_grammar_errors(paragraph)  # Assuming it returns indices of errors
        if error_indices:
            grammar_errors.append((idx, error_indices))

    # Print results
    print("Spelling Corrected Paragraphs:")
    for i, corrected in enumerate(corrected_paragraphs):
        print(f"Paragraph {i + 1} \n\t Original: \t{paragraphs[i]}")
        print(f"  \tCorrected: \t{corrected}")

    crctr = corrector()
    print("Grammar Errors:")
    for idx, error_indices in grammar_errors:
        print(f"Paragraph {idx + 1} has grammatical errors at indices: {error_indices}")
        for start, end in error_indices:
            print(f"  Error range: [{start}:{end}] => {corrected_paragraphs[idx][start:end]}")
            print(f"  Corrected phrase : {crctr.correct_grammar(corrected_paragraphs[idx][start:end])}")


from GrammarChecker.GrammarChecker import GrammarChecker as gc
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
        "මම ඊයේ උද්‍යානයට ගියා, ළමයි ටිකක් පැසිපන්දු ක්‍රීඩා කරනවා දැක්කා. මමයි මලලියි එයාලට සෙල්මකට එකකතු වුණා. අපි "
        "එහෙමට මෙහෙට දුවලා හිනාවෙලා හරිම විනෝදයෙන් හිටියා. පසුවබ ඔවුන්ගෙන් එක් අබයෙක් අපට ඔවුන්ගේ නිවසට කෙටි ආහාර සඳහා "
        "ආරාධනා කළේය. එදා අලුත් යාලුඑමවො ගැන මට ලොකු සතුටක් දැනුනා.",
        "පවුලේ අය සමඟ කාලය ගත කිරීම කොතරම් වැදගත්ද යන්න අපට බොහෝ විරට අමතක වේ. මමයි නංගිබයි තීරණය කළා ඊයේ රෑ හැමෝටම රෑට "
        "කෑම හදන්න. ඇය සෝස් සූදානම් කරන අතරතුර මම එළවළු කපා දැමුවෙමි. අපේ දෙමව්පියෝ අපිත් එක්ක කෑම මේසෙටර ගියාම එයාලා "
        "අපිට ප්‍රශංසා කළා උත්සාහය ගැන. ඒක අපිව ළං කළා.",
        "මට අද මගේ අට්ටාලයේ පැරිණි සඟරාවක් හමු විය. එය මගේ ආච්චිට අයත් වූ අතර ඇගේ වචන කියවීම කාලය හරහා ගමන් කිරීමක් "
        "වැනිය. ඇය තම පවුලට ආදරය කළ ආකාරැය ගැන ලිවීය. මම සරහ මගේ ඥාති සහෝදරියන් ඇයගේ ගෞරවය පිණිස සීරීම් පොතවක් සෑදීමට "
        "තීරණය කළා. ඇගේ උරුමය රැකගැනීම ගැන අපට ආඩම්රයක් දැනුණා.",
        "වෙරළ තීරය ජනාකීර්ණ වූ නමුත් විශාල ගස්ක සෙවන යට නිස්කලංක ස්ථානයක් සොයා ගැනීමට අපට හැකි විය. මමයි මගේ යාළුවොයි "
        "වැලි මාලිගා හදලා සාගරයේ පීනා ගියා. මම සිහිවටනන ලෙස මුහුදු කටු පවා එකතු කළා. හොඳම දේ තමයි ආගන්තුකයෙක් අපිට "
        "අයිස්ක්‍රීම් පිරිනැමීම. එය මගේ දවස විය!",
        "මම මගේ නිදහස් කාලය තුළ පින්තාරු කිරීමට කැමතියි. මමයි මගේ මිතුරායි අපේ අසල්වැසි ප්‍රදේශයේ කුඩා කලා සමාජයක් "
        "ආරම්භ කළා. අපි සෑම සති අන්තයකම අදහස් හුවමාරු කරර ගැනීමට සහ ව්‍යාපෘතිවල වැඩ කිරීමට හමුවෙමු. පසුගිය සතියේ මම "
        "හිරු බැස යෑමක් පින්තාරු කටළ අතර, හැමෝම එයට කැමති විය. අපගේ කලාකරුවන් වර්ණ සහ හැඩයතල තුළින් අපගේ අදහස් ප්‍රකාශ "
        "කිරීමන් සතුටක් ලබන්නෙමු."
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
    print("Corrected Paragraphs:")
    for i, corrected in enumerate(corrected_paragraphs):
        print(f"Paragraph {i + 1}:\n{corrected}")

    print("Grammar Errors:")
    for idx, error_indices in grammar_errors:
        print(f"Paragraph {idx + 1} has grammatical errors at indices: {error_indices}")
        for start, end in error_indices:
            print(f"  Error range: [{start}:{end}] => {corrected_paragraphs[idx][start:end]}")

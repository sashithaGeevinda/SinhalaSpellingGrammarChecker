from openai import OpenAI
import os


class GrammarCorrector:
    def __init__(self):
        """Initialize the GrammarCorrector with GPT API key."""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")

        self.client = OpenAI(api_key=self.api_key)

        # Knowledge Base: Sinhala grammar rules
        self.grammar_rules = {
            "මම": "Sentences starting with 'මම' as subject should have verb ending in 'මි'.",
            "අපි": "Sentences starting with 'අපි' as subject should have verb ending in 'මු'."
        }

    def build_context(self, paragraph):
        """Build context dynamically based on word presence in the paragraph."""
        context = """Correct the following paragraph for Sinhala grammar errors and only output the corrected sentence.

Grammar Rules:
"""
        for word, rule in self.grammar_rules.items():
            if word in paragraph:
                context += f"- {rule}\n"
        context += f"\nParagraph:\n{paragraph}"
        return context

    def correct_grammar(self, paragraph):
        """Use GPT-4 API to correct grammar in the given paragraph."""
        context = self.build_context(paragraph)

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": context}
                ],
                model="gpt-4o-mini",
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error has occurred: most likely the subscription for gpt-4o-mini used for this chatbot has expired"


# Example usage
if __name__ == "__main__":
    paragraph = "අපි ඊයේ වෙරළ තීරයේ හිරු බැස යෑම නැරඹීමෙන් සතුටක් ලැබුවා."
    try:
        corrector = GrammarCorrector()
        corrected_paragraph = corrector.correct_grammar(paragraph)
        print("Corrected Paragraph:")
        print(corrected_paragraph)
    except Exception as error:
        print(error)

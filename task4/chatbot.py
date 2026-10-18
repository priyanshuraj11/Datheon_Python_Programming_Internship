import json
import re
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "sample_faq.json"

EXIT_COMMANDS = {"bye", "goodbye", "exit", "quit"}

THANKS_PATTERNS = [
    r"\bthank you\b",
    r"\bthanks\b",
    r"\bthx\b"
]

HELP_PATTERNS = [
    r"\bhelp\b",
    r"\bwhat can you do\b",
    r"\bhow can you help\b"
]

PRODUCT_PATTERNS = [
    r"\bproduct\b",
    r"\bproducts\b",
    r"\bprice\b",
    r"\bcost\b",
    r"\bfeatures?\b",
    r"\bavailable\b",
    r"\bavailability\b"
]


class RuleBasedChatbot:

    def __init__(self, data_file=DATA_FILE):
        self.data_file = Path(data_file)
        self.data = self.load_data()
        self.state = "greeting"
        self.faqs = self.data.get("faqs", [])
        self.greetings = [
            item.lower().strip()
            for item in self.data.get("greetings", [])
            if isinstance(item, str)
        ]

    def load_data(self):
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Chatbot data file not found: {self.data_file}"
            ) from exc

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Invalid JSON format in chatbot_data.json"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError("The JSON dataset must contain an object.")

        if not isinstance(data.get("greetings", []), list):
            raise ValueError("'greetings' must be a list.")

        if not isinstance(data.get("faqs", []), list):
            raise ValueError("'faqs' must be a list.")

        for index, faq in enumerate(data.get("faqs", []), start=1):
            if not isinstance(faq, dict):
                raise ValueError(f"FAQ entry {index} must be an object.")

            if not isinstance(faq.get("question"), str):
                raise ValueError(f"FAQ entry {index} needs a question.")

            if not isinstance(faq.get("answer"), str):
                raise ValueError(f"FAQ entry {index} needs an answer.")

        return data

    @staticmethod
    def normalize(text):
        text = text.lower().strip()
        text = re.sub(r"[^\w\s'-]", " ", text)
        text = re.sub(r"\s+", " ", text)

        return text

    @staticmethod
    def contains_any(text, patterns):
        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in patterns
        )

    @staticmethod
    def token_set(text):
        return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))

    def find_faq(self, message):
        normalized_message = self.normalize(message)
        message_tokens = self.token_set(normalized_message)

        best_faq = None
        best_score = 0.0

        for faq in self.faqs:
            question = self.normalize(faq["question"])
            question_tokens = self.token_set(question)

            if not question_tokens:
                continue

            if normalized_message == question:
                return faq

            overlap = len(message_tokens & question_tokens)

            precision = overlap / max(len(message_tokens), 1)
            recall = overlap / max(len(question_tokens), 1)

            if precision + recall:
                score = (
                    2 * precision * recall
                    / (precision + recall)
                )
            else:
                score = 0.0

            if question in normalized_message:
                score = max(score, 0.95)

            if score > best_score:
                best_score = score
                best_faq = faq

        if best_faq and best_score >= 0.34:
            return best_faq

        return None

    def greeting_response(self, message):
        normalized = self.normalize(message)

        for greeting in sorted(self.greetings, key=len, reverse=True):
            if normalized == greeting or re.search(
                rf"\b{re.escape(greeting)}\b",
                normalized
            ):
                return (
                    "Hello! I am your support assistant. "
                    "You can ask about business hours, "
                    "project submission, or certificates."
                )

        return None

    def identify_intent(self, message):
        normalized = self.normalize(message)

        if normalized in EXIT_COMMANDS:
            self.state = "exit"

            return "Goodbye! Thank you for contacting support."

        greeting = self.greeting_response(message)

        if greeting:
            self.state = "intent_identification"
            return greeting

        if self.contains_any(normalized, THANKS_PATTERNS):
            self.state = "resolution"

            return (
                "You're welcome! "
                "Is there anything else I can help you with?"
            )

        if self.contains_any(normalized, HELP_PATTERNS):
            self.state = "intent_identification"

            return (
                "I can help with business hours, "
                "internship project submission, "
                "and certificate processing."
            )

        faq = self.find_faq(message)

        if faq:
            self.state = "resolution"
            return faq["answer"]

        if self.contains_any(normalized, [
            r"\bhour\b",
            r"\bhours\b",
            r"\bopen\b",
            r"\bclosing\b",
            r"\bworking days\b"
        ]):
            self.state = "resolution"

            return (
                "Our business hours are Monday through Friday, "
                "from 9:00 AM to 6:00 PM IST."
            )

        if self.contains_any(normalized, [
            r"\bintern(ship)?\b",
            r"\bsubmit\b",
            r"\bsubmission\b",
            r"\bgithub\b",
            r"\brepository\b",
            r"\bworkspace\b"
        ]):
            self.state = "resolution"

            return (
                "You can submit your public GitHub repository "
                "link through your Student Workspace."
            )

        if self.contains_any(normalized, [
            r"\bcertificate\b",
            r"\bcertification\b",
            r"\bissued\b"
        ]):
            self.state = "resolution"

            return (
                "Certificates are reviewed and issued within "
                "3-5 business days after your code review."
            )

        if self.contains_any(normalized, PRODUCT_PATTERNS):
            self.state = "resolution"

            return (
                "I don't have product catalogue or pricing "
                "details in the current dataset. "
                "Please contact a support representative "
                "for product-specific information."
            )

        self.state = "intent_identification"

        return (
            "I'm not sure I understood that question. "
            "You can ask about business hours, project submission, "
            "or certificates. Type 'help' for supported topics."
        )

    def respond(self, message):
        if self.state == "exit":
            return (
                "This conversation has ended. "
                "Run the program again to restart."
            )

        if not message or not message.strip():
            return (
                "Please enter a question or type 'help' "
                "to see supported topics."
            )

        return self.identify_intent(message.strip())

    def run(self):
        print("=" * 60)
        print("       RULE-BASED CUSTOMER SUPPORT CHATBOT")
        print("=" * 60)

        print(
            "Bot: Hello! Ask me about business hours, "
            "project submission, or certificates."
        )

        print(
            "Bot: Type 'help' for assistance or "
            "'bye', 'exit', or 'quit' to finish."
        )

        print("-" * 60)

        while self.state != "exit":
            try:
                user_message = input("You: ")

            except (EOFError, KeyboardInterrupt):
                print(
                    "\nBot: Goodbye! "
                    "Thank you for contacting support."
                )

                self.state = "exit"
                break

            response = self.respond(user_message)

            print(f"Bot: {response}\n")


def main():
    try:
        chatbot = RuleBasedChatbot()
        chatbot.run()

    except (FileNotFoundError, ValueError) as error:
        print(f"Startup error: {error}")


if __name__ == "__main__":
    main()
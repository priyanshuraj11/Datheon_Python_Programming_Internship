

b2683500-9137-42c5-af86-3df72c1bee7b.json
File
Detailed Problem Statement & Requirements

Implement a rule-based customer support or product assistant. The bot parses user input for keywords and regular expressions, handles queries regarding business hours, product FAQs, and returns contextual responses. It includes fallback handling for unrecognized queries and clean exit commands ('bye', 'exit', 'quit').

Suggested Technical Approach

1. Create 'chatbot.py'. 2. Define intent response dictionaries or load questions from a JSON dataset. 3. Normalize user input (lowercase, strip whitespace, regex keyword extraction). 4. Implement conversational state management (greeting -> intent identification -> resolution -> exit). 5. Provide graceful fallbacks when query confidence is low.

Recommended Tools:Python 3re (regex)json code do compelte and detaiked no comment


Neeche complete Rule-Based Customer Support Chatbot ka code hai. Isme comments nahi hain, jaisa aapne bola. Aapki attached JSON file mein diye gaye greetings aur 3 FAQs ko bhi use kiya hai: business hours, internship project submission, aur certificate processing. 


Project files download: 

1. Folder Structure
Rule_Based_Chatbot/
│
├── chatbot.py
├── chatbot_data.json
└── README.md
2. chatbot.py — Complete Code
import json
import re
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent / "chatbot_data.json"

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
3. chatbot_data.json
Aapki attached JSON file ko isi naam se chatbot.py ke saath rakhein.

{
    "greetings": [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon"
    ],
    "faqs": [
        {
            "question": "What are your hours of operation?",
            "answer": "We operate Monday through Friday from 9:00 AM to 6:00 PM IST."
        },
        {
            "question": "How do I submit my internship project?",
            "answer": "You can submit your public GitHub repository link through your Student Workspace."
        },
        {
            "question": "When will I receive my certificate?",
            "answer": "Certificates are reviewed and issued within 3-5 business days after your code review."
        }
    ]
}
4. Run karne ka command
Terminal mein project folder open karein aur execute karein:

python chatbot.py
Kisi additional package ko install karne ki zaroorat nahi hai.

5. Example Output
============================================================
       RULE-BASED CUSTOMER SUPPORT CHATBOT
============================================================
Bot: Hello! Ask me about business hours, project submission, or certificates.
Bot: Type 'help' for assistance or 'bye', 'exit', or 'quit' to finish.
------------------------------------------------------------
You: hello
Bot: Hello! I am your support assistant. You can ask about business hours, project submission, or certificates.

You: What are your business hours?
Bot: We operate Monday through Friday from 9:00 AM to 6:00 PM IST.

You: How do I submit my internship project?
Bot: You can submit your public GitHub repository link through your Student Workspace.

You: When will I receive my certificate?
Bot: Certificates are reviewed and issued within 3-5 business days after your code review.

You: bye
Bot: Goodbye! Thank you for contacting support.
Features included
Keyword matching: User ke message se relevant intent identify karta hai.

Regex matching: Patterns se greetings aur supported queries identify karta hai.

JSON-based FAQs: Questions aur answers alag file mein store hote hain.

Conversation state: Greeting, intent identification, resolution aur exit states maintain hote hain.

Fallback handling: Unknown query par helpful response deta hai.

Graceful exit: bye, exit, aur quit commands support karta hai.

Error handling: Missing ya invalid JSON dataset ke liye error message deta hai.

Note: Ye rule-based chatbot hai, AI/LLM chatbot nahi. Product-specific answers tabhi dega jab aap unke questions aur answers chatbot_data.json mein add karenge. 


ab in 4 ki readme .md bana do downlloadble bas overview summanry type banana github ke liye for this entire repo 

Main 3 projects identify kar paaya hoon:

Investment Portfolio — portfolio.py, stock_list.csv

Smart File Organizer — organizer.py

Rule-Based Chatbot — chatbot.py, chatbot_data.json

4th project ka naam bata do. Uske baad main chaaron repositories ke liye separate, downloadable README.md files bana dunga — GitHub-ready format mein, sirf overview, project summary, key features, tech stack aur basic usage ke saath. 📄




Ad
Ads do not influence the answers you get from ChatGPT. Your chats stay private. 
Learn about ads and personalization

readme.md banan do overall 

Overall GitHub repository ke liye README.md bana diya hai. 📄


Isme included hai:

Project Overview — repository ka overall summary

Projects — Investment Portfolio, Smart File Organizer aur Rule-Based Chatbot

Technology Stack — Python, JSON aur CSV

Getting Started — basic run commands

Repository Structure

Purpose & License

GitHub par use kaise karein: Download karke apne main repository folder mein README.md naam se rakho aur GitHub par push kar do.

Note: README available project details par based hai. Agar chautha project bhi isi repository ka part hai, toh uska section add karna hoga. 



README.md


Project Portfolio
A collection of practical Python projects focused on automation, data handling, and conversational support. Each project is designed to demonstrate a specific use case with a simple, easy-to-understand implementation.

Projects
1. Investment Portfolio
A Python-based portfolio utility that works with stock data stored in a CSV file.

Main files

portfolio.py

stock_list.csv

2. Smart File Organizer
A Python utility for organizing files into categories based on their file types, helping keep directories structured and easier to navigate.

Main file

organizer.py

3. Rule-Based Chatbot
A lightweight customer-support chatbot that uses a JSON knowledge base to respond to greetings and frequently asked questions. It also handles common intents such as help, thanks, and exit commands.

Main files

chatbot.py

chatbot_data.json

Technology
Python

JSON for chatbot knowledge data

CSV for stock-list data

Standard Python libraries for core functionality

Getting Started
Clone or download this repository.

Open the folder for the project you want to run.

Check the files and any project-specific data files.

Run the relevant Python script from a terminal.

For example, to start the rule-based chatbot:

python chatbot.py
To run the file organizer, use:

python organizer.py
Run each command from the directory containing the corresponding script. If a project has additional instructions or options, refer to its own documentation.

Repository Structure
.
├── portfolio.py
├── stock_list.csv
├── organizer.py
├── chatbot.py
├── chatbot_data.json
└── README.md
The exact folder structure may vary depending on how the projects are organized in your repository.

Purpose
This repository serves as a compact portfolio of Python projects demonstrating basic data handling, automation, and rule-based response logic.

License
No license has been specified. Add a license file if you want to define how others may use, modify, or distribute this project.


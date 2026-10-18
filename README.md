Python Mini Projects

Task 1: Hangman Game

Problem Statement:
Develop a terminal-based Hangman game in which the player guesses a hidden word one letter at a time, with a maximum of six incorrect attempts. The game should display ASCII gallows art that changes after each incorrect guess, track guessed letters, and prevent duplicate guesses from reducing the remaining attempts.

Solution Approach:
Create hangman.py and select a secret word randomly from a predefined list or an English word dataset using Python's random module. Track guessed letters with a set, display the word with unguessed letters masked, and update the gallows after each incorrect guess until the player wins or runs out of attempts.

Task 2: Investment Portfolio Tracker

Problem Statement:
Build a utility that lets users enter stock ticker symbols, purchase prices, and share quantities. It should calculate the total invested amount, current portfolio value, and percentage gain or loss for each holding, then save a transaction summary to a CSV file.

Solution Approach:
Create portfolio.py and store portfolio positions in a suitable data structure, such as a dictionary. Obtain stock prices from the provided CSV dataset or a live market-data source, calculate each holding's invested value and gain or loss, and write the results to portfolio_summary.csv using Python's built-in csv module.

Task 3: Smart File Organizer

Problem Statement:
Develop a desktop file-organization utility that scans a cluttered directory, identifies files by extension, creates category folders such as Documents, Images, Videos, Archives, and Code, and moves files into the appropriate folders. It should handle permission errors and filename collisions safely.

Solution Approach:
Create organizer.py with an extension-to-category mapping. Use os.scandir() or pathlib to inspect files and shutil.move() to move them into dynamically created folders. Add exception handling for permission and file conflicts, and print a summary of how many files were moved.

Task 4: Rule-Based Customer Support Chatbot

Problem Statement:
Build a rule-based customer support or product assistant that interprets user messages using keywords and regular expressions. It should answer questions about business hours and FAQs, provide fallback responses for unknown queries, and exit cleanly when the user enters commands such as bye, exit, or quit.

Solution Approach:
Create chatbot.py and define response rules or load FAQs from a JSON dataset. Normalize input by converting it to lowercase and removing unnecessary whitespace, then identify intents using keywords, regular expressions, or simple matching logic. Manage the conversation flow from greeting to intent identification, resolution, and exit, with a fallback when no suitable answer is found.

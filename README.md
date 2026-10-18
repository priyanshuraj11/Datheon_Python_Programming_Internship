

b2683500-9137-42c5-af86-3df72c1bee7b.json
File
Detailed Problem Statement & Requirements

Implement a rule-based customer support or product assistant. The bot parses user input for keywords and regular expressions, handles queries regarding business hours, product FAQs, and returns contextual responses. It includes fallback handling for unrecognized queries and clean exit commands ('bye', 'exit', 'quit').

Suggested Technical Approach

1. Create 'chatbot.py'. 2. Define intent response dictionaries or load questions from a JSON dataset. 3. Normalize user input (lowercase, strip whitespace, regex keyword extraction). 4. Implement conversational state management (greeting -> intent identification -> resolution -> exit). 5. Provide graceful fallbacks when query confidence is low.

Recommended Tools:Python 3re (regex)json code do compelte and detaiked no comment


Short summary-style README bana diya hai, jisme sirf Problem Statement aur Solution hain.

📄 Download

GitHub repository ke liye concise aur suitable format hai. 



all task 1 2 3 4 ki problem statement and usko kaise solve karenge uski readme bana do task 1 ki problem statemnt and solutoin then task 2 3 4 aise 

Task 1, 2, 3 aur 4 ke liye ek hi README.md bana dunga. Har task mein sirf Problem Statement aur Solution Approach ke 1–2 short paragraphs honge.

Abhi available details:

Task 1: Investment Portfolio

Task 2: Smart File Organizer

Task 3: Rule-Based Chatbot

Task 4: Iska naam ya problem statement mere paas available nahi hai.

Task 4 ka naam ya screenshot bhej do. Main chaaron tasks ki combined, downloadable README.md file bana dunga.


Detailed Problem Statement & Requirements

Develop a terminal-based Hangman game where the user attempts to guess a hidden word letter by letter within 6 attempts. Implement visual ASCII gallows art that updates with each incorrect guess, tracks previously guessed letters, and prevents duplicate penalty deduction.

Suggested Technical Approach

1. Create 'hangman.py'. 2. Download the provided English word list or define a secret word array. 3. Use random.choice() to select a word. 4. Track correctly guessed letters in a set and display a masked string (e.g. '_ A _ H E O N'). 5. Limit mistakes to 6 and display corresponding ASCII stage art for each incorrect guess.

Recommended Tools:Python 3VS Code / PyCharmStandard Library (random)

Download English Words List (.TXT) → Detailed Problem Statement & Requirements

Build an investment portfolio tracking utility. The program allows users to enter stock ticker symbols, buy prices, and share quantities. It computes total portfolio value, percentage gain/loss per holding, and automatically logs the transaction summary to an external CSV file.

Suggested Technical Approach

1. Create 'portfolio.py'. 2. Store portfolio positions in a dictionary structure. 3. Look up current ticker prices (from the sample CSV or live via requests/yfinance). 4. Calculate total invested capital vs current market value. 5. Write results into 'portfolio_summary.csv' using Python's built-in csv module.

Recommended Tools:Python 3csv moduleFile IO

Download S&P 500 Ticker Dataset (.CSV) → Detailed Problem Statement & Requirements

Construct an autonomous desktop automation utility that organizes cluttered directories (e.g., Downloads folder). The script inspects every file's extension, dynamically creates category subfolders (/Documents, /Images, /Videos, /Archives, /Code), and safely moves files while handling permission exceptions and naming collisions.

Suggested Technical Approach

1. Create 'organizer.py'. 2. Define an extension mapping dictionary: {'.pdf': 'Documents', '.jpg': 'Images', '.png': 'Images', '.zip': 'Archives'}. 3. Use os.scandir() and shutil.move() to relocate files. 4. Implement try-except blocks to catch FileExistsError or PermissionError. 5. Print a formatted execution summary showing total files relocated.

Recommended Tools:Python 3osshutilpathlib

View Python File Handling Docs ↗ Detailed Problem Statement & Requirements

Implement a rule-based customer support or product assistant. The bot parses user input for keywords and regular expressions, handles queries regarding business hours, product FAQs, and returns contextual responses. It includes fallback handling for unrecognized queries and clean exit commands ('bye', 'exit', 'quit').

Suggested Technical Approach

1. Create 'chatbot.py'. 2. Define intent response dictionaries or load questions from a JSON dataset. 3. Normalize user input (lowercase, strip whitespace, regex keyword extraction). 4. Implement conversational state management (greeting -> intent identification -> resolution -> exit). 5. Provide graceful fallbacks when query confidence is low.

Recommended Tools:Python 3re (regex)json

Download Sample FAQ Dataset (.JSON) → ye rahe ab do


Chaaron tasks ki combined GitHub-ready README.md bana di hai. Har task mein Problem Statement aur Solution Approach diya gaya hai, based on your provided requirements.

📄 Download README.md

Isme included hai:

Task 1: Hangman Game

Task 2: Investment Portfolio Tracker

Task 3: Smart File Organizer

Task 4: Rule-Based Customer Support Chatbot

README concise hai, jise directly apni GitHub repository mein add kar sakte ho. 



Library
/
README.md



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


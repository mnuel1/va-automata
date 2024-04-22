import nltk
import random

actions = {
    "General Actions": ["play", "pause", "stop", "call", "send", "compose", "volume up", "volume down"],
    "Task Management": ["set", "add", "create", "edit", "delete", "remind", "schedule", "snooze"],
    "Information Retrieval": ["what", "when", "why", "where", "how"],  
    "Confirmation": ["yes", "no", "maybe"],
    "Feedback": ["thanks", "cancel", "repeat"]
}

# Define a CFG for simple commands
grammar = nltk.CFG.fromstring("""
    S -> Command
    Command -> OpenProgram | Greet | Unknown
    OpenProgram -> 'can' 'you' 'open' Program
    Program -> 'google chrome' | 'spotify' | 'visual studio code'
    Greet -> 'hello' | 'hi' | 'hey' 
    Unknown -> 'i' 'do' 'not' 'understand' 'that'
""")


# Define a function to generate a response based on the parsed tree
def generate_response(parsed_tree):
    for subtree in parsed_tree[0]:
        if subtree.label() == 'OpenProgram':
            program = ' '.join(subtree.leaves()[3:])
            return f"Opening {program}..."
        elif subtree.label() == 'Greet':
            return random.choice(["Hello!", "Hi!", "Hey!"])
    return "I do not understand that."

sentences = [
    "Open the door",
    "Close the window",
    "Play some music",
    "Pause the video",
    "Stop the alarm",
    # "Find my phone",
    # "Search for restaurants nearby",
    # "Show me the weather forecast",
    # "Call John",
    # "Text mom",
    # "Send an email to Mike",
    # "Compose a message",
    # "Write a note",
    # "Volume up the speaker",
    # "Volume down the TV",
    # "Set a reminder for tomorrow",
    # "Add an event to my calendar",
    # "Create a new task",
    # "Edit the document",
    # "Delete the file",
    # "Remind me to buy groceries",
    # "Schedule a meeting for Monday",
    # "Snooze the alarm for 10 minutes",
    # "What time is it?",
    # "When is the next train?",
    # "Why is the sky blue?",
    # "Where is the nearest coffee shop?",
    # "How do I get to the airport?",
    # "Yes, I confirm the appointment",
    # "No, I don't want to proceed",
    # "Maybe, let me think about it",   
    # "Thanks for the reminder",
    # "Cancel the operation",
    # "Repeat the message please"
]

for sentence in sentences:
    try:
        # user_input = input("You: ").lower()
        user_input = sentence.lower()
        tokens = nltk.word_tokenize(user_input)
        parser = nltk.ChartParser(grammar)
        if parser:
            for tree in parser.parse(tokens):
                response = generate_response(tree)
                print("Bot:", response)
                break  # Only consider the first parse treez
        else:
            print("Bot:", "I do not understand that.")
    except ValueError as e:
        print("Bot:", "Error:", e)
    # action, subject = identify_action_and_subject(sentence)
    # print("Sentence:", sentence)
    # print("Action:", action)
    # print("Subject:", subject)
    # print()

# Main conversation loop
# print("Bot: Hello! How can I assist you today?")
# while True:
#     try:
#         user_input = input("You: ").lower()
#         tokens = nltk.word_tokenize(user_input)
#         parser = nltk.ChartParser(grammar)
#         if parser:
#             for tree in parser.parse(tokens):
#                 response = generate_response(tree)
#                 print("Bot:", response)
#                 break  # Only consider the first parse tree
#         else:
#             print("Bot:", "I do not understand that.")
#     except ValueError as e:
#         print("Bot:", "Error:", e)
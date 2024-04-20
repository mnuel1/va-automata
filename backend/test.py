import re

# Word categories (improved for subject extraction)
word_categories = {
  "General Actions": ["open", "close", "play", "pause", "stop", "find", "search", "show", "call", "text", "send", "compose", "write"],
  "Task Management": ["set", "add", "create", "edit", "delete", "remind", "schedule", "snooze"],
  "Information Retrieval": ["what", "when", "why", "where", "how"],
  "Entertainment": ["play", "pause", "skip", "next", "previous", "volume up", "volume down"],
  "Confirmation": ["yes", "no", "maybe"],
  "Feedback": ["thanks", "cancel", "repeat"]
}

def extract_keywords_and_subject(sentence):
  """
  Extracts the action category and potential subject from a sentence.
  (Optional: Uses POS tagging for improved subject extraction)
  """
  words = sentence.lower().split()
  action_category = None
  subject = None

  # Optional: Use POS tagging (replace with your implementation)
  # tagged_words = nltk.pos_tag(words)  # Example using NLTK

  for i, word in enumerate(words):
    if word in word_categories:
      action_category = word_categories[word]
      break  # Exit loop if action verb is found

    # Look for noun phrases following action verbs (without POS tagging)
    if action_category and i + 1 < len(words) and not any(tag in word for tag in ["VB", "VBZ", "MD"]):  # Skip verbs and modals
      subject = " ".join(words[i + 1:])  # Consider words after the action verb
      break  # Exit loop after finding potential subject

  return action_category, subject

# Example usage
sentence1 = "What will be the weather tomorrow?"
sentence2 = "Can you open a program?"
sentence3 = "Set a reminder for 8 pm"
sentence4 = "Search the web for NLP concepts"

action1, subject1 = extract_keywords_and_subject(sentence1)
action2, subject2 = extract_keywords_and_subject(sentence2)
action3, subject3 = extract_keywords_and_subject(sentence3)
action4, subject4 = extract_keywords_and_subject(sentence4)

if action1:
  print(f"Sentence 1: Action - {action1}, Subject - {subject1}")  # Output: None, None
else:
  print("Sentence 1: No keywords found.")

# ... (and so on for other sentences)

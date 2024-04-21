import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def identify_action_and_subject(sentence):
    # Tokenize the sentence
    words = word_tokenize(sentence)
    # Tag the parts of speech
    tagged_words = pos_tag(words)
    print(tagged_words)
    # Identify the action (verb) and the subject (noun or pronoun)
    action = None
    subject = None
    for word, pos in tagged_words:
        if pos.startswith('V'):  # Verb
            action = word
        elif pos.startswith('N'):  # Noun or pronoun
            subject = word
    return action, subject

# Example sentences


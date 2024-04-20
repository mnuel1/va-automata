#!/usr/bin/env python
# coding: utf-8

# In[40]:


import nltk
from nltk.tokenize import word_tokenize


# In[59]:


rules = [
    (r'(The|the|A|a|An|an)$', 'AT'),  # articles
    (r'.*able$', 'ADJ'),               # adjectives
    (r'.*ly$', 'ADV'),                 # adverbs
    (r'.*([a-zA-Z]+(ed|ing|es|s|en))$|(IS|is|Am|am|Are|are|Was|was|Were|were)$', 'VB'),   #verb
    (r'(He|he|She|she|It|it|I|Me|me|You|you|His|his|Her|her|Its|its|They|they|We|we|Them|them|Their|their)$', 'PRP'), #pronouns
    (r'(To|to|In|in|On|on|Of|of|For|for|With|with)$', 'PRE'),   # prepositions
    (r'(And|and|Or|or|But|but)$', 'CN'),  # conjunctions
    (r'[,.;?()"]', 'PUN'),              # punctuation
    (r'.*', 'NN')                     # default: nouns
]


# In[60]:


# Create a regex-based tagger based on the rules
regexp_tagger = nltk.RegexpTagger(rules)


# In[61]:


# Define a sample sentence to test the tagger
sample_sentence = "He is a good dog. He guards the house every day."


# In[62]:


# Tokenize the sample sentence
tokens = word_tokenize(sample_sentence)


# In[63]:


# Tag the tokens using the regex-based tagger
tagged_tokens = regexp_tagger.tag(tokens)


# In[64]:


# Print the tagged tokens
print(tagged_tokens)


# In[ ]:




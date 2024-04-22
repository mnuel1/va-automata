import nltk

#  make at least the inquiry flexible
# Define the CFG rules
cfg_rules = """
    S -> OPEN_PROGRAM | INQUIRY     
    OPEN_PROGRAM -> MODAL PRONOUNS VERB NOUN_PHRASE | VERB NOUN | VERB ADJECTIVE NOUN | VERB NOUN_PHRASE | VERB NOUN_PHRASE PREP_PHRASE | VERB NOUN_PHRASE PREP_PHRASE    
    INQUIRY -> QUESTION VERB DETERMINERS NOUN PUNCTUATIONS | QUESTION VERB NOUN PUNCTUATIONS | QUESTION NOUN PUNCTUATIONS | QUESTION VERB DETERMINERS NOUN | QUESTION VERB NOUN | QUESTION NOUN | QUESTION VERB DETERMINERS NOUN ADJECTIVE PUNCTUATIONS | QUESTION VERB NOUN ADJECTIVE PUNCTUATIONS | QUESTION NOUN ADJECTIVE PUNCTUATIONS | QUESTION VERB DETERMINERS NOUN ADJECTIVE | QUESTION VERB NOUN ADJECTIVE | QUESTION NOUN ADJECTIVE 
    
    
    NOUN_PHRASE -> DETERMINERS NOUN | DETERMINERS ADJECTIVE NOUN | ADJECTIVE NOUN
    PREP_PHRASE -> PREPOSITIONS NOUN_PHRASE

    PUNCTUATIONS -> "?"
    QUESTION -> "what" | "when" | "why" | "where" | "how"
    MODAL -> "can"
    PRONOUNS -> "you"   
    NOUN -> "computer" | "microsoft" | "word" | "spotify" | "chrome" | "firefox" | "skype" | "zoom" | "excel" | "powerpoint" | "outlook" | "photoshop" | "illustrator" | "indesign" | "premiere" | "aftereffects" | "audition" | "acrobat" | "wordpad" | "notepad" | "visualstudio" | "eclipse" | "androidstudio" | "unity" | "unrealengine" | "blender" | "autocad" | "solidworks"  
    ADJECTIVE -> "microsoft" | "important"
    VERB  ->  "open" | "close" | "is" | "search"
    DETERMINERS -> "the"        
    PREPOSITIONS -> "in"
"""

# Create CFG parser
grammar = nltk.CFG.fromstring(cfg_rules)
parser = nltk.ChartParser(grammar)

# Example prompts
prompts = [
    "can you open microsoft word",
    "open the microsoft word",
    "open microsoft word",
    "can you close skype",
    "close the microsoft word",
    "close microsoft word",
    "what is the computer",
    "what is computer",
    "why is the computer important ?",
    "why computer important ?"
    
]

# Parse prompts
for prompt in prompts:
    tokens = nltk.word_tokenize(prompt)    
    try:
        trees = list(parser.parse(tokens))        
        if not trees:
            print(f"I am sorry, I don't understand your task: {prompt}")
        else:
            for tree in trees:
                print(tree)
    except ValueError as e:
        print(f"Error parsing input: {prompt}. Error: {e}")
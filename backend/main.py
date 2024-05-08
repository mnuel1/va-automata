import nltk
from flask import Flask, request, jsonify


app = Flask(__name__)

class TalkieChum:    

    # Define the CFG rules
    cfg_rules = """
        S -> PROGRAM_ACTIONS |
        PROGRAM_ACTIONS -> MODAL PRONOUNS VERB PROGRAM_NOUN | VERB PROGRAM_NOUN |         
        
        PROGRAM_NOUN -> DETERMINERS PROGRAM | DETERMINERS ADJECTIVE PROGRAM | ADJECTIVE PROGRAM | PROGRAM   
        PREP_PHRASE -> PREPOSITIONS PROGRAM_NOUN
            
        PROGRAM -> "microsoft" | "word" | "spotify" | "chrome" | "firefox" | "skype" | "zoom" | "excel" | "powerpoint" | "outlook" | "photoshop" | "illustrator" | "indesign" | "premiere" | "aftereffects" | "audition" | "acrobat" | "wordpad" | "notepad" | "visualstudio" | "eclipse" | "androidstudio" | "unity" | "unrealengine" | "blender" | "autocad" | "solidworks"
        
        MODAL -> "can"
        PRONOUNS -> "you"   
                
        ADJECTIVE -> "microsoft" | "important"
        VERB  ->  "open" | "close" | "is" | "search"
        DETERMINERS -> "the"
        PREPOSITIONS -> "in"
        PUNCTUATIONS -> "?"
    """

    def __init__(self, prompt):
        self.prompt = prompt
        # Create CFG parser
        grammar = nltk.CFG.fromstring(self.cfg_rules)
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
            tokens = nltk.word_tokenize(prompt.lower())    
            if not (self.isQuestion(tokens)):
                try:
                    trees = list(parser.parse(tokens))        
                    if not trees:
                        print(f"I am sorry, I don't understand your task: {prompt}")
                    else:
                        for tree in trees:
                            print(tree)
                except ValueError as e:
                    print(f"I am sorry, I don't understand your task: {prompt}. Error: {e}")

    def isQuestion(tokens):
        return any(token.lower() in ["what", "when", "why", "where", "how"] for token in tokens)


# talkie_chum = TalkieChum()

# @app.route('/parse_prompt', methods=['POST'])
# def parse_prompt():
#     data = request.get_json()
#     prompt = data['prompt']
#     result = talkie_chum.parse_prompt(prompt)
#     return jsonify(result)


# if __name__ == "__main__":
#     app.run(debug=True)


if __name__ == "__main__":
    # Example usage
    user_prompt = input("What would you like to browse for? ")
    browser = TalkieChum(user_prompt)
    
import nltk
from flask import Flask, request, jsonify
import webbrowser

app = Flask(__name__)

class TalkieChum:    

    # Define the CFG rules
    cfg_rules = """
        
    """

    def __init__(self, prompt):
        self.prompt = prompt
        # Create CFG parser
        grammar = nltk.CFG.fromstring(self.cfg_rules)
        parser = nltk.ChartParser(grammar)

        # Parse prompts
        tokens = nltk.word_tokenize(prompt.lower())
        
        if not self.isQuestion(tokens):  # Removed parentheses around self.isQuestion
            try:
                trees = list(parser.parse(tokens))        
                if not trees:
                    print(f"I am sorry, I don't understand your task: {prompt}")
                else:
                    for tree in trees:
                        print(tree)
            except ValueError as e:
                print(f"I am sorry, I don't understand your task: {prompt}. Error: {e}")
        else : 
            print(f"Unfortunately, I do not understand your request, but the web says")
            url = f"https://www.google.com/search?q={prompt.lower()}"
            webbrowser.open(url)

    def isQuestion(self, tokens):  # Added self parameter
        return any(token.lower() in ["what", "when", "why", "where", "how"] for token in tokens)


# talkie_chum = TalkieChum()

# @app.route('/parse_prompt', methods=['POST'])
# def parse_prompt():
#     data = request.get_json()
#     prompt = data['prompt']
#     result = talkie_chum.parse_prompt(prompt)
#     return jsonify(result)


# if __name__ == '__main__':
#   app.run(host='127.0.0.1', port=4000)



if __name__ == "__main__":
    # Example usage
    user_prompt = input("What would you like to browse for? ")
    browser = TalkieChum(user_prompt)

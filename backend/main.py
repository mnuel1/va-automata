# import re
# from datetime import datetime, timedelta

# # Predefined data
# knowledge_base = {
#     "weather_today": "The weather is sunny today.",
#     "weather_tomorrow": "The weather will be partly cloudy tomorrow.",
#     "time": "The current time is 10:00 AM.",
#     "greeting": "Hello! How can I assist you?",
#     "farewell": "Goodbye! Have a great day!"
# }

# # Function to perform semantic search
# def semantic_search(query):
#     query = query.lower()
#     intent, parameters = extract_intent(query)
    
#     if intent == "weather_today":
#         return knowledge_base.get("weather_today", "Sorry, I don't have information about the weather.")
#     elif intent == "weather_tomorrow":
#         return knowledge_base.get("weather_tomorrow", "Sorry, I don't have information about the weather for tomorrow.")
#     elif intent == "time":
#         return knowledge_base.get("time", "Sorry, I don't have information about the time.")
#     elif intent == "greeting":
#         return knowledge_base.get("greeting")
#     elif intent == "farewell":
#         return knowledge_base.get("farewell")
#     else:
#         return "Sorry, I didn't understand that."

# # Function to extract intent and parameters from the query
# def extract_intent(query):
#     query = query.lower()
#     intent = None
#     parameters = None
    
#     # Define patterns for different intents
#     weather_today_pattern = r'weather\s*(?:today|now)'
#     weather_tomorrow_pattern = r'weather\s*(?:tomorrow|next day)'
#     time_pattern = r'(time|current time|current)'
#     greeting_pattern = r'(hello|hi|hey)'
#     farewell_pattern = r'(goodbye|bye)'
    
#     # Match patterns in the query
#     if re.search(weather_today_pattern, query):
#         intent = "weather_today"
#     elif re.search(weather_tomorrow_pattern, query):
#         intent = "weather_tomorrow"
#     elif re.search(time_pattern, query):
#         intent = "time"
#     elif re.search(greeting_pattern, query):
#         intent = "greeting"
#     elif re.search(farewell_pattern, query):
#         intent = "farewell"
    
#     return intent, parameters

# # Main function
# def main():
#     print("Welcome to Simple Virtual Assistant!")
#     print("You can ask me about weather, time, or just say hello.")
    
#     while True:
#         user_input = input("You: ").strip()
        
#         if user_input.lower() == "exit":
#             print("Assistant: Goodbye!")
#             break
        
#         response = semantic_search(user_input)
#         print("Assistant:", response)

# if __name__ == "__main__":
#     main()

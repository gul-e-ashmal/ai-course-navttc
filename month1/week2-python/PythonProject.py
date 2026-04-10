import random
from datetime import datetime

print("WELCOME TO CHATBOT!!! \nType quit for exit")

responses = {
    "greeting": ["Hello! How can I help you?", "Hi there!", "Hey! Nice to meet you!"],
    "farewell": ["Goodbye! Have a great day!", "See you later!", "Bye! Come back soon!"],
    "thanks": ["You're welcome!", "Happy to help!", "My pleasure!"],
    "default": ["Interesting... tell me more.", "I see. Please continue.", "That's fascinating!"]
}

greeting_keywords = ["hello", "hi", "hey", "greetings"]
farewell_keywords = ["bye", "goodbye", "see you", "later"]
thanks_keywords = ["thanks", "thank you", "appreciate it"]

question_patterns = {
    "how are you": "I'm doing great, thanks for asking! How about you?",
    "what is your name": "I'm Chatbot, your virtual assistant!",
    "what can you do": "I can chat with you, answer basic questions, calculate, and remember our conversation!",
    "what version": "I'm version 1.0",
    "what time": f"The current time is {datetime.now().strftime('%H:%M')}",
    "what date": f"Today's date is {datetime.now().strftime('%Y-%m-%d')}"
}

def get_response(message):
    message = message.lower()
    
    if any(keyword in message for keyword in greeting_keywords):
        return random.choice(responses["greeting"])
    
    elif any(keyword in message for keyword in farewell_keywords):
        return random.choice(responses["farewell"])
    
    elif any(keyword in message for keyword in thanks_keywords):
        return random.choice(responses["thanks"])
    
    elif "calculate" in message or any(op in message for op in ['+', '-', '*', '/']):
        try:
            # Type conversion example
            for op in ['+', '-', '*', '/']:
                if op in message:
                    parts = message.split(op)
                    num1 = float(parts[0].strip())
                    num2 = float(parts[1].strip())
                    
                    if op == '+':
                        result = num1 + num2
                    elif op == '-':
                        result = num1 - num2
                    elif op == '*':
                        result = num1 * num2
                    elif op == '/':
                        if num2 == 0:
                            return "Error: Cannot divide by zero!"
                        result = num1 / num2
                    
                    return f"Result: {result}"
        except (ValueError, IndexError):
            return "Invalid input. Please enter valid numbers like: 5 + 3"
    
    for pattern, response in question_patterns.items():
        if pattern in message:
            return response
    
    return random.choice(responses["default"])

while True:
    print("Chatbot: Hello! How can I help you?")
    message = input("You: ")
    
    if message.lower() == "quit":
        print("Chatbot: Goodbye! Have a great day!")
        break
    
    response = get_response(message)
    print(f"Chatbot: {response}")



# Test scenarios:
# 1. "hello"           # Greeting response
# 2. "how are you"     # Question pattern
# 3. "5 + 3"           # Calculation
# 4. "10 / 2"          # Division
# 5. "5 / 0"           # Division by zero error
# 6. "thank you"       # Thanks response
# 7. "bye"             # Farewell
# 8. "quit"            # Exit program


from flask import Blueprint, request, jsonify
import re
import random

# Create a blueprint for the bot routes
bot_bp = Blueprint('bot', __name__)


# Bot configuration
BOT_NAME = "Honey"

# Predefined responses
R_EATING = f"I don't like eating anything because I'm a {BOT_NAME} obviously!"
R_ADVICE = "Stay focused and constantly moving to make your dreams come true!"

# Predefined answers for specific questions
THINK_ANSWERS = {
    "what is the meaning of life?": "The meaning of life is a philosophical question concerning the significance of life or existence in general.",
    "how does the internet work?": "The internet is a global network of interconnected computers that communicate via standardized protocols.",
}

def message_probability(user_message, recognised_words, single_response=False, required_words=None):
    """
    Calculate the probability of a user's message matching a predefined response.

    :param user_message: List of words in the user's message.
    :param recognised_words: List of words associated with a predefined response.
    :param single_response: Whether the response requires exact match or not.
    :param required_words: Words that must be present for a match.
    :return: Probability score (0-100).
    """
    message_certainty = sum(word in recognised_words for word in user_message)
    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    if required_words:
        has_required_words = all(word in user_message for word in required_words)
    else:
        has_required_words = True

    return int(percentage * 100) if has_required_words or single_response else 0

def check_all_messages(message):
    """
    Check the user's message against predefined responses and return the best match.

    :param message: List of words in the user's message.
    :return: Best matching response or unknown response.
    """
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=None):
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Add responses
    response(f'How can I help you? I\'m {BOT_NAME}!', ['hello', 'hi', 'hey'], single_response=True)
    response('My name is Honey', ['name'], single_response=True)
    response('<a href="http://localhost:5173/contact">Contact</a>', ['job', 'assignment'], single_response=True)
    response('<a href="mailto:socialwing02@gmail.com">Email Me</a>', ['gmail'], single_response=True)
    response('<a href="ph:8015544800">Contact</a>', ['Contact','number'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Love you too!', ['i', 'love', 'you'], required_words=['love'])
    response('I\'m happy to chat with you!', ['bye', 'thank', 'thanks', 'goodbye'], single_response=True)
    response(R_ADVICE, ['give', 'advice'], required_words=['advice'])
    response('CHRISTAL', ['build', 'generate', 'design'], single_response=True)
    response(R_EATING, ['what', 'you', 'eat'], required_words=['you', 'eat'])

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return unknown() if highest_prob_list[best_match] < 1 else best_match

def unknown():
    """
    Return a default response when the bot cannot understand the user's message.

    :return: Default response.
    """
    return random.choice(["What does that mean?", "I'm not sure I understand.", "Could you rephrase that?"])

@bot_bp.route('/bot', methods=['POST'])
def bot_response():
    """
    Endpoint to handle user input and return the bot's response.

    :return: JSON response with the bot's message.
    """
    user_input = request.json.get('message', '')
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())

    # Check for predefined answers
    if user_input.lower() in THINK_ANSWERS:
        return jsonify({'response': THINK_ANSWERS[user_input.lower()]})

    # Generate response based on user input
    response = check_all_messages(split_message)
    return jsonify({'response': response})




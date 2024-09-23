import random
import nltk
import spacy
import wikipediaapi  # For fetching definitions from Wikipedia
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('nps_chat')

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Initialize stopwords
stop_words = set(stopwords.words('english'))

# Initialize Wikipedia API with a proper User-Agent
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent="MyChatbot/1.0 (no website; siddiquimaaz94@gmail.com)"
)

# Sample responses based on user input
RESPONSES = {
    "greeting": ["Hi there! How can I help you today?", "Hello! What would you like to talk about?", "Hey! How's it going?"],
    "goodbye": ["Goodbye! Have a great day!", "See you later!", "Take care!"],
    "thanks": ["You're welcome!", "No problem!", "Glad to help!"],
    "default": ["I'm sorry, I don't understand that.", "Can you please clarify?", "Let's talk about something else."]
}

# Load the NPS chat corpus
posts = nltk.corpus.nps_chat.xml_posts()

# Convert corpus data into a dataset for training
def prepare_training_data():
    X = []
    y = []
    for post in posts:
        X.append(post.text)
        y.append(post.get('class'))
    return X, y

# Train a Naive Bayes classifier using the NPS chat corpus
def train_classifier(X, y):
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create a pipeline that converts text to a matrix of token counts, then applies Naive Bayes
    model = make_pipeline(CountVectorizer(), MultinomialNB())

    # Train the model
    model.fit(X_train, y_train)

    # Evaluate the model (optional)
    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    return model

# Function to fetch definitions from Wikipedia
def fetch_definition(term):
    page = wiki_wiki.page(term)
    if page.exists():
        return page.summary.split('.')[0]  # Return the first sentence from the summary
    else:
        return "I'm sorry, I couldn't find a definition for that term."

# Generate a response based on the predicted intent or keywords
def generate_response(intent, user_input):
    # Convert user input to lowercase for easy keyword matching
    user_input_lower = user_input.lower()

    # Handle keywords like "thanks" explicitly
    if any(word in user_input_lower for word in ["thanks", "thank you", "thank"]):
        return random.choice(RESPONSES["thanks"])

    # Handle conversational keywords
    if any(word in user_input_lower for word in ["ok", "okay", "fine"]):
        return "Got it! Let's move on."

    if any(word in user_input_lower for word in ["no", "nah", "nothing"]):
        return "Alright, let me know if you change your mind."

    # Greet response
    if intent == "Greet":
        return random.choice(RESPONSES["greeting"])
    
    # Goodbye response
    elif intent == "Bye":
        return random.choice(RESPONSES["goodbye"])

    # Check if user is asking for a definition (e.g., "What is...")
    elif "what is" in user_input_lower:
        term = user_input_lower.replace("what is", "").strip()
        if term:
            return fetch_definition(term)
        else:
            return "Can you specify what you'd like me to define?"

    # Default fallback response
    return random.choice(RESPONSES["default"])

# Main chatbot loop
def chatbot(model):
    print("Chatbot: Hello! I am a simple chatbot. Type 'bye' to exit.")

    while True:
        user_input = input("You: ")
        if "bye" in user_input.lower():
            print("Chatbot: " + random.choice(RESPONSES["goodbye"]))
            break

        # Predict the intent of the user's input
        predicted_intent = model.predict([user_input])[0]

        # Generate a response based on the intent and user input
        response = generate_response(predicted_intent, user_input)
        print("Chatbot: " + response)

# Run the chatbot
if __name__ == "__main__":
    # Prepare the training data
    X, y = prepare_training_data()

    # Train the classifier
    model = train_classifier(X, y)

    # Start the chatbot
    chatbot(model)

# # Main code 
# from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# import openai
# import time
# import pyttsx3

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
# db = SQLAlchemy(app)
# openai.api_key = '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'

# class ChatHistory(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_input = db.Column(db.String(255))
#     chacha_response = db.Column(db.String(255))
#     image_url = db.Column(db.String(255))

# def chat_with_chacha(user_input):
#     # Your existing chat_with_chacha function
#     restricted_keywords = ['rivers','who', 'river', 'namami gange', 'Hi', 'Bye', 'namami ganga plan', 'namami ganga', 'chacha chaudhary', 'ganga', 'river conservation', 'namami ganga project']
#     if any(keyword.lower() in user_input.lower() for keyword in restricted_keywords):
#         retries = 3
#         for _ in range(retries):
#             try:
#                 response = openai.ChatCompletion.create(
#                     model="gpt-3.5-turbo",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant."},
#                         {"role": "user", "content": user_input},
#                     ]
#                 )
#                 return response['choices'][0]['message']['content']
#             except openai.error.RateLimitError as e:
#                 time.sleep(5)
#         raise Exception("Exceeded rate limits even after retries.")
#     else:
#         return "Sorry, I can't access this type of information which is aprt from this project."

# def generate_image_url(user_input):
#     # Your existing generate_image_url function
#     try:
#         image = openai.Image.create(
#             prompt=user_input,
#             n=1,
#             size="256x256"
#         )
#         return image['data'][0]['url']
#     except openai.error.OpenAIError as e:
#         return f"Error generating image: {str(e)}"

# def speak(text=250, max_words=150):
#     # Your existing speak function
#     words = text.split()[:max_words]
#     truncated_text = ' '.join(words)

#     engine = pyttsx3.init()
#     engine.say(truncated_text)
#     engine.runAndWait()

# @app.route('/')
# def chat_page():
#     # Retrieve all conversation history from the database
#     all_history = ChatHistory.query.all()
#     return render_template('index.html', chat_history=all_history)


# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.form['user_input']
#     response = chat_with_chacha(user_input)

#     k = user_input.split()
#     images = ['rivers', 'river', 'namami gange', 'namami ganga plan', 'namami ganga', 'chacha chaudhary', 'ganga','river conservation']
#     image_url = None
#     for i in k:
#         if i in images:
#             image_url = generate_image_url(user_input)

#     # Save the conversation to the database
#     save_to_database(user_input, response, image_url)

#     # Retrieve all conversation history from the database
#     all_history = ChatHistory.query.all()

#     return render_template('index.html', user_input=user_input, chacha_response=response, image_url=image_url, chat_history=all_history)

# def save_to_database(user_input, chacha_response, image_url):
#     chat_history = ChatHistory(user_input=user_input, chacha_response=chacha_response, image_url=image_url)
#     db.session.add(chat_history)
#     db.session.commit()

# if __name__ == '__main__':  
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)






# from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# import openai
# import time
# import pyttsx3
# import re

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
# db = SQLAlchemy(app)
# openai.api_key = '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'

# class ChatHistoryModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_input = db.Column(db.String(255))
#     chacha_response = db.Column(db.String(255))
#     image_url = db.Column(db.String(255))

# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)

# class ChatHistory:
#     def __init__(self, user_input, chacha_response, image_url):
#         self.user_input = user_input
#         self.chacha_response = chacha_response
#         self.image_url = image_url

# def truncate_to_last_sentence(text, max_words):
#     sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
#     truncated_text = ''
#     for sentence in sentences:
#         if len(truncated_text.split()) + len(sentence.split()) <= max_words:
#             truncated_text += sentence + ' '
#         else:
#             break
#     return truncated_text.strip()

# def chat_with_chacha(user_input):
#     retries = 3
#     for _ in range(retries):
#         try:
#             response = openai.ChatCompletion.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant."},
#                     {"role": "user", "content": user_input},
#                 ]
#             )

#             max_word_limit_output = 150
#             output_content = response['choices'][0]['message']['content']
#             truncated_output = truncate_to_last_sentence(output_content, max_word_limit_output)

#             return truncated_output
#         except openai.error.RateLimitError as e:
#             time.sleep(5)
#     raise Exception("Exceeded rate limits even after retries.")

# def generate_image_url(user_input):
#     images = ['rivers', 'river', 'namami gange', 'namami ganga plan', 'namami ganga', 'chacha chaudhary', 'ganga namami', 'gange namami']
    
#     if any(x.lower() in user_input.lower() for x in images):
#         image = openai.Image.create(
#             prompt=user_input,
#             n=1,
#             size="512x512"
#         )
#         return image['data'][0]['url']
#     else:
#         return None

# def speak(audio, rate=150):
#     engine.setProperty('rate', rate)
#     engine.say(audio)
#     engine.runAndWait()

# @app.route('/')
# def chat_page():
#     all_history = ChatHistoryModel.query.all()
#     return render_template('index.html', chat_history=all_history)

# @app.route('/chat', methods=['POST'])
# def chat_with_chacha_route():
#     user_input = request.form['user_input']
#     response = chat_with_chacha(user_input)
#     image_url = generate_image_url(user_input)
    
#     chat_history = ChatHistoryModel(user_input=user_input, chacha_response=response, image_url=image_url)
#     # Save the conversation to the database
#     save_to_database(chat_history)

#     # Retrieve all conversation history from the database
#     all_history = ChatHistoryModel.query.all()

#     # Speak the response
#     speak(response)

#     return render_template('index.html', chat_history=[chat_history])

# def save_to_database(chat_history):
#     db.session.add(chat_history)
#     db.session.commit()

# if __name__ == '__main__':  
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)









# Main code 
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openai
import time
import pyttsx3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
db = SQLAlchemy(app)
openai.api_key = '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'

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.String(255))
    chacha_response = db.Column(db.String(255))
    image_url = db.Column(db.String(255))

def chat_with_chacha(user_input):
    # Your existing chat_with_chacha function
    restricted_keywords = ['rivers','who', 'river', 'namami gange', 'Hi', 'Bye', 'namami ganga plan', 'namami ganga', 'chacha chaudhary', 'ganga', 'river conservation', 'namami ganga project']
    if any(keyword.lower() in user_input.lower() for keyword in restricted_keywords):
        retries = 3
        for _ in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": user_input},
                    ]
                )
                return response['choices'][0]['message']['content']
            except openai.error.RateLimitError as e:
                time.sleep(5)
        raise Exception("Exceeded rate limits even after retries.")
    else:
        return "Sorry, I can't access this type of information which is apart from this project."

def generate_image_url(user_input):
    # Your existing generate_image_url function
    try:
        image = openai.Image.create(
            prompt=user_input,
            n=1,
            size="256x256"
        )
        return image['data'][0]['url']
    except openai.error.OpenAIError as e:
        return f"Error generating image: {str(e)}"

def speak(text, max_words=150):
    # Adjust the speak function to limit the output to max_words
    words = text.split()[:max_words]
    truncated_text = ' '.join(words)

    engine = pyttsx3.init()
    engine.say(truncated_text)
    engine.runAndWait()

@app.route('/')
def chat_page():
    # Retrieve all conversation history from the database
    all_history = ChatHistory.query.all()
    return render_template('index.html', chat_history=all_history)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    response = chat_with_chacha(user_input)

    k = user_input.split()
    images = ['rivers', 'river', 'namami gange', 'namami ganga plan', 'namami ganga', 'chacha chaudhary', 'ganga','river conservation']
    image_url = None
    for i in k:
        if i in images:
            image_url = generate_image_url(user_input)

    # Save the conversation to the database
    save_to_database(user_input, response, image_url)

    # Retrieve all conversation history from the database
    all_history = ChatHistory.query.all()

    # Speak the response with a maximum of 150 words
    speak(response, max_words=150)

    return render_template('index.html', user_input=user_input, chacha_response=response, image_url=image_url, chat_history=all_history)

def save_to_database(user_input, chacha_response, image_url):
    chat_history = ChatHistory(user_input=user_input, chacha_response=chacha_response, image_url=image_url)
    db.session.add(chat_history)
    db.session.commit()

if __name__ == '__main__':  
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# dev.py
from app import app, initialize_chatbot

if __name__ == '__main__':
    initialize_chatbot()
    app.run(debug=True)
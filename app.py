# app.py
from flask import Flask, render_template, request, jsonify
from main import setup, MemoryContext
from waitress import serve
import os

app = Flask(__name__)

# Global variables to store setup results
query_handler = None
responder = None
memory = None
is_initialized = False

def initialize_chatbot():
    global query_handler, responder, memory, is_initialized
    if not is_initialized:
        print("Initializing chatbot...")
        query_handler, responder, memory = setup()
        is_initialized = True

@app.before_request
def before_request():
    initialize_chatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data['question']
    
    context = query_handler.handle(question)
    memory_context = memory.get_context()
    full_context = f"{memory_context}\n\n{context}"
    
    answer = responder.respond(question, full_context)
    
    if "technical difficulties" not in answer and "unable to provide an answer" not in answer:
        memory.add(question, answer)
    
    return jsonify({'answer': answer})

if __name__ == '__main__':
    # Initialize the chatbot
    initialize_chatbot()
    
    # Use Waitress as the production server
    print("Starting server...")
    serve(app, host='127.0.0.1', port=5000)
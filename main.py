import os
from settings import Settings
from text_processor import FolderProcessor
from embedder import Embedder
from db_manager import DBManager
from query_handler import QueryHandler
from responder import Responder
from timings import logger
import time

class MemoryContext:
    def __init__(self, max_history=5):
        self.history = []
        self.max_history = max_history
        self.current_context = None

    def add(self, question, answer):
        self.history.append((question, answer))
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def set_current_context(self, context):
        self.current_context = context

    def get_context(self):
        context = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in self.history])
        if self.current_context:
            context += f"\n\nCurrent context: {self.current_context}"
        return context

def setup():
    try:
        Settings.check()
        
        embedder = Embedder()
        db = DBManager(embedder)
        
        # Process new text files
        new_documents = FolderProcessor.process_folder()
        if new_documents:
            db.add_docs(new_documents)
        else:
            logger.info("No new files to process.")
        
        query_handler = QueryHandler(db)
        responder = Responder()
        memory = MemoryContext()
        
        logger.info("Setup complete")
        return query_handler, responder, memory
    except Exception as e:
        logger.error(f"Setup error: {str(e)}")
        raise

def run():
    try:
        query_handler, responder, memory = setup()
        
        while True:
            query = input("Ask a question (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            context = query_handler.handle(query, memory)
            
            answer = responder.respond(query, context, memory)
            print(f"Answer: {answer}")
            
            if "technical difficulties" not in answer and "unable to provide an answer" not in answer:
                memory.add(query, answer)
                # Update the current context based on the question and answer
                memory.set_current_context(f"{query} - {answer[:100]}...")
            else:
                print("Apologies for the inconvenience. Please wait a moment before asking another question.")
                time.sleep(10)  
    except Exception as e:
        logger.error(f"Runtime error: {str(e)}")

if __name__ == "__main__":
    run()
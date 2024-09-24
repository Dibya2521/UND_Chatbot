from timings import time_it, logger
from groq import Groq
from settings import Settings
import tiktoken
import time

class Responder:
    def __init__(self):
        self.client = Groq(api_key=Settings.GROQ_KEY)
        self.model = Settings.GROQ_MODEL
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = 32768

    def _trim_context(self, context, query, max_tokens):
        sys_prompt = "You are a helpful assistant specializing in answering questions based on the provided context. Provide accurate and comprehensive information based on the given context."
        query_prompt = f"Question: {query}\n\nPlease provide a comprehensive and detailed answer based on the given context and conversation history. If the information is not available, please say so."
        
        fixed_tokens = len(self.encoder.encode(sys_prompt + query_prompt))
        available_tokens = max_tokens - fixed_tokens - 8000 

        context_tokens = self.encoder.encode(context)
        if len(context_tokens) > available_tokens:
            context_tokens = context_tokens[:available_tokens]
        
        return self.encoder.decode(context_tokens)

    @time_it
    def respond(self, query, context):
        max_retries = 3
        retry_delay = 10  # seconds

        for attempt in range(max_retries):
            try:
                trimmed_context = self._trim_context(context, query, self.max_tokens)
                
                prompt = f"""
                Context:
                {trimmed_context}

                Current question: {query}

                Please provide a comprehensive, detailed, and informative answer based on the given context. If the information is not available or if you're unsure about any point, please say so. Your response should be thorough and at least 150 words long.
                """

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant specializing in answering questions based on the provided context. Provide accurate and comprehensive information based on the given context."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=8000 
                )

                answer = response.choices[0].message.content
                logger.info(f"Generated response for: '{query}'")
                return answer.strip()
            except Exception as e:
                if "rate_limit_exceeded" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"Rate limit exceeded. Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Error generating response: {str(e)}")
                    return "I apologize, but I'm currently experiencing technical difficulties. Please try again later or rephrase your question."

        return "I'm sorry, but I'm unable to provide an answer at this time due to technical issues. Please try again later."
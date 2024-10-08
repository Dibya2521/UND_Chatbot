from timings import time_it, logger
from openai import OpenAI
from settings import Settings
import tiktoken
import time

class Responder:
    def __init__(self):
        self.client = OpenAI(api_key=Settings.OPENAI_API_KEY)
        self.model = "gpt-4o"
        self.encoder = tiktoken.get_encoding("cl100k_base")
        self.max_tokens = 8192

    def _trim_context(self, context, query, max_tokens):
        sys_prompt = "You are a knowledgeable staff member at the University of North Dakota. Provide direct, accurate, and concise responses."
        query_prompt = f"""
        Question: {query}
        Please provide a direct and specific answer to the question, without using phrases like 'based on the given information or context' or 'according to the context.' If certain details are not available, mention it clearly only once and avoid elaborating on missing information.
        """

        
        fixed_tokens = len(self.encoder.encode(sys_prompt + query_prompt))
        available_tokens = max_tokens - fixed_tokens - 1000  # Reserve tokens for the response

        context_tokens = self.encoder.encode(context)
        if len(context_tokens) > available_tokens:
            context_tokens = context_tokens[:available_tokens]
        
        return self.encoder.decode(context_tokens)

    @time_it
    def respond(self, query, context, memory):
        max_retries = 3
        retry_delay = 10  # seconds

        for attempt in range(max_retries):
            try:
                trimmed_context = self._trim_context(context, query, self.max_tokens)
                
                memory_context = memory.get_context()
                
                prompt = f"""
                You are a knowledgeable staff member at the University of North Dakota. Your goal is to provide direct, accurate, and concise responses.

                Here's the information available to answer the question:

                {trimmed_context}

                Current question: {query}

                Previous conversation context:
                {memory_context}

                Please follow these guidelines:

                1. Respond directly to the specific question without using phrases like 'based on the given information,' 'according to the context,' or similar expressions. If information is missing, state it clearly and only once, for example, "The exact information is not available."
                2. Provide all relevant and available information related to the question in a single response to ensure completeness. Do not split related details across multiple responses.
                3. Include partial information where exact details are missing. For example, if only the cost of some parts of the program is available, provide that, and specify that other details are not available.
                4. Provide consistent and comprehensive answers. Include every relevant aspect (e.g., costs, duration, different levels like BS, MS) in one response when applicable.
                5. Focus on delivering relevant and specific information. Avoid providing unrelated or tangential information that does not directly answer the question.
                6. Avoid repeating the same line multiple times in the response. State missing information once without redundancy.
                7. Avoid phrases like 'Additional Information' or 'given context.' Instead, respond directly and concisely to the question.
                8. When multiple details are available (e.g., tuition fees, program fees, additional costs), list them all clearly and systematically. Do not omit any relevant details that can help answer the question comprehensively.
                9. Consider previous conversation context when answering follow-up questions. Ensure the response is relevant and cohesive based on the prior discussion.
                10. If certain details are unknown or unavailable, state that briefly without elaboration, and provide the closest relevant information you have.
                11. Speak as if you are directly communicating with the person asking the question, giving the impression of a knowledgeable staff member.
                12. Remember, you are responding as an expert, not as an AI model or a third party. Avoid sounding detached or overly formal.

                Your objective is to provide a direct, informative, and complete answer based on the information provided, covering all relevant details without introducing unnecessary elaborations or repetitions.
                """

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are a knowledgeable staff member at the University of North Dakota. Provide direct, accurate, and concise responses, without using any phrases such as 'based on the given information or context' or 'according to the context.' Just give the answer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.5,
                    max_tokens=4000 
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
                    return "I'm sorry, but I can't access that information right now. Could you please ask your question again in a moment?"

        return "I apologize, but I'm having some technical issues at the moment. Could you please try asking your question again later?"
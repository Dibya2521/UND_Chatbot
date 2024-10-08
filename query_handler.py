from timings import time_it, logger

class QueryHandler:
    def __init__(self, db_manager):
        self.db = db_manager

    @time_it
    def handle(self, query, memory=None):
        try:
            docs = self.db.search(query)
            context = self._format_context(docs)
            
            # If memory is provided and has current_context, include it in the search
            if memory and hasattr(memory, 'current_context') and memory.current_context:
                context_docs = self.db.search(memory.current_context)
                context += "\n\n" + self._format_context(context_docs)
            
            logger.info(f"Handled query: '{query}' with {len(docs)} relevant docs")
            return context
        except Exception as e:
            logger.error(f"Error handling query: {str(e)}")
            return []

    def _format_context(self, documents):
        context = []
        for doc in documents:
            context.append(f"Text: {doc.page_content}")
        return "\n\n".join(context)
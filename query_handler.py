from timings import time_it, logger

class QueryHandler:
    def __init__(self, db_manager):
        self.db = db_manager

    @time_it
    def handle(self, query):
        try:
            docs = self.db.search(query)
            context = self._format_context(docs)
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
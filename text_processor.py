from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from settings import Settings
from timings import time_it, logger

class TextProcessor:
    @staticmethod
    @time_it
    def process_text(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=Settings.CHUNK_SIZE,
                chunk_overlap=Settings.CHUNK_OVERLAP,
                length_function=len,
            )
            chunks = splitter.split_text(text)
            
            documents = [Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks]
            logger.info(f"Processed {file_path} into {len(documents)} chunks")
            return documents
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return []
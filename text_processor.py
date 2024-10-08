import os
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

class FolderProcessor:
    @staticmethod
    @time_it
    def process_folder():
        all_documents = []
        processed_files_path = os.path.join(Settings.TEXT_FILES_FOLDER, 'processed_files.txt')
        
        try:
            # Load processed files
            processed_files = set()
            if os.path.exists(processed_files_path):
                with open(processed_files_path, 'r') as f:
                    processed_files = set(f.read().splitlines())
            
            # Process new files
            new_files_processed = False
            for filename in os.listdir(Settings.TEXT_FILES_FOLDER):
                file_path = os.path.join(Settings.TEXT_FILES_FOLDER, filename)
                
                if filename.endswith('.txt') and filename != 'processed_files.txt' and file_path not in processed_files:
                    logger.info(f"Processing new file: {filename}")
                    documents = TextProcessor.process_text(file_path)
                    all_documents.extend(documents)
                    
                    # Mark file as processed
                    with open(processed_files_path, 'a') as f:
                        f.write(f"{file_path}\n")
                    new_files_processed = True

            if new_files_processed:
                logger.info(f"Processed new files in {Settings.TEXT_FILES_FOLDER}. Total new documents: {len(all_documents)}")

            return all_documents
        except Exception as e:
            logger.error(f"Error processing folder {Settings.TEXT_FILES_FOLDER}: {str(e)}")
            return []
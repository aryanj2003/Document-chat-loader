from openai import OpenAI, RateLimitError
from tenacity import retry, stop_after_attempt, wait_random_exponential

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
client = OpenAI(api_key='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')

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6), retry_error_callback=lambda x: isinstance(x, RateLimitError))
def completion_with_backoff(**kwargs):
    return client.completions.create(**kwargs)

# Example usage
try:
    result = completion_with_backoff(model="gpt-3.5-turbo-instruct", prompt="Once upon a time,")
    print(result)
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.response.headers.get('Retry-After')} seconds.")








import os
import shutil

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader

CHROMA_PATH = "chroma"
DATA_PATH = "Books/Data"


def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks


def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    try:
        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(openai_api_key="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"), persist_directory=CHROMA_PATH
        )
        db.persist()
        print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")
    except RateLimitError as e:
        print(f"Rate limit exceeded. Retry after {e.response.headers.get('Retry-After')} seconds.")


if __name__ == "__main__":
    main()

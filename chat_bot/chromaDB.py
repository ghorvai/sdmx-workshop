import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from uuid import uuid4 as uuid
import os
from dotenv import load_dotenv

class ChromaDBWrapper:
    def __init__(  self
                 , flat_info_for_embedding
                 , openai_api_key=None
                 , collection_name="dataflow-meta-information-embeddings"):
        self.flat_info_for_embedding = flat_info_for_embedding
        self.collection_name = collection_name
        
        load_dotenv()
        if openai_api_key is None:
            openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(settings=Settings(anonymized_telemetry=False), path='.chroma.db')
        
        # Set up embedding function
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            model_name='text-embedding-3-small',
            api_key=openai_api_key
        )
        
        # Create or get the collection
        self.create_collection()
        
        # Add data to the collection
        self.add_data_to_collection()

    def create_collection(self):
        # # Clear the collection if it already exists
        try:
            self.client.get_collection(name=self.collection_name, embedding_function=self.embedding_function)
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.create_collection(name=self.collection_name, embedding_function=self.embedding_function)
        except:
            self.collection = self.client.create_collection(name=self.collection_name, embedding_function=self.embedding_function)
        print(f"Collection {self.collection_name} created successfully")


    def add_data_to_collection(self):
        ids = []
        documents = []
        metadatas = []

        for question, answer in self.flat_info_for_embedding:
            ids.append(str(uuid()))
            documents.append(str(question))
            metadatas.append({"answer": answer})

        to_vectorize = {'ids': ids, 'documents': documents, 'metadatas': metadatas}
        self.collection.add(**to_vectorize)
        print(f"{len(ids)} embeddings created from documents were and added to the vector store.")

    def query(self, query_text, n_results=3):
        result_sets = self.collection.query(query_texts=[query_text], n_results=n_results)
        return result_sets

# Example usage:
if __name__ == "__main__":
    # Assuming flat_info_for_embedding is defined
    flat_info_for_embedding = [
        ("What is the code for lower secondary education?", "The code for lower secondary education is 2."),
        # Add more question-answer pairs here
    ]

    # Create an instance of ChromaDBWrapper
    chroma_wrapper = ChromaDBWrapper(flat_info_for_embedding)

    # Query the collection
    query_text = 'What is the code for the lower secondary education?'
    results = chroma_wrapper.query(query_text)

    print(f"The most similar question to '{query_text}' is: \n\t{results['documents'][0][0]}")
    print(f"The answer to the question is: \n\t{results['metadatas'][0][0]['answer']}")
import LLM
from SDMX_DataFlow import Dataflow
from data_prep_for_indenxing import flatten_info
from chromaDB import ChromaDBWrapper

class Bot:
    def __init__(self, dataflow_name):
        self.dataflow_name = dataflow_name
        self.chroma_wrapper = self.setup_vector_store()

    def setup_vector_store(self):
        dataflow_details_url = self._get_dataflow_url_from_name(self.dataflow_name)

        # Create an instance of the Dataflow class and populate the variables
        df_info = Dataflow(dataflow_details_url)

        print("Populating variables...")
        df_info.populate_variables()
        print("Variables populated.")

        # Flatten the dataflow information for embedding
        flat_info_for_embedding = flatten_info(df_info)

        # Create the document store
        print("Creating the document store...")
        chroma_wrapper = ChromaDBWrapper(flat_info_for_embedding) 

        return chroma_wrapper

    def _get_dataflow_url_from_name(self, dataflow_name):
        # Split the dataflow_name into agency and the rest
        agency, rest = dataflow_name.split(':')
        
        # Split the rest into id and version
        id_part, version = rest.split('(')
        
        # Remove the closing parenthesis from the version
        version = version.rstrip(')')
        
        # Return the dataflow url
        return f'https://sdmx.oecd.org/public/rest/dataflow/{agency}/{id_part}/{version}?references=all'

    def answer_question(self, user_question):
        # Get the 3 most relevant entries from the vector store
        result_sets = self.chroma_wrapper.query(user_question, n_results=3)

        # Generate the answer to the user question
        persona = """You are a helpful data analyst working for OECD."""
        prompt = f"""
        Please provide the answer to the following user question: 
        {user_question}
        Please use the information from the source that was selected as the best source to answer the question!
        These are the most similar questions to the user question:
        '''{result_sets['documents'][0]}'''
        
        The metadata in your knowledgebase that corresponds most to the questions are:
        '''{result_sets['metadatas']}'''
        
        Very important: Not having any relevant information in your knowledgebase related to the user's question is likely and acceptable. So, please make sure to:
            - ask for clarification, if the question is not clear.
            - let the user know if you don't have relevant information in your knowledgebase. 
        """

        ans, cost = LLM.model(persona, prompt)
        return ans

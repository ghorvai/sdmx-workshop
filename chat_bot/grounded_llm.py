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
        chroma_wrapper = ChromaDBWrapper(flat_info_for_embedding) # should be called with the api key (since i already need it for the LLM)

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
        # Get the most similar question and answer from the vector store
        result_sets = self.chroma_wrapper.query(user_question, n_results=3)

        # Generate the answer to the user question
        persona = """You are a helpful data analyst working for OECD."""
        prompt = f"""
        Please provide the answer to the following user question: 
        {user_question}
        Please use the information from the source that was selected as the best source to answer the question!
        This is the most similar question to the user question:
        '''{result_sets['documents'][0]}'''
        
        The metadata in your knowledgebase that corresponds most to the question is:
        '''{result_sets['metadatas'][0][0]['answer']}'''
        Very important: if you don't have relevant information in your knowledgebase, please let the user know.
        """

        ans, cost = LLM.model(persona, prompt)
        return ans










# # Define the dataflow URL <= this will come from the dropdown selection of the chatbot
# fin_perstud = {"agency": "OECD.EDU.IMEP",
# "id": "DSD_EAG_UOE_FIN@DF_UOE_INDIC_FIN_PERSTUD",
# "version": "1.0"}

# dataflow_details_url = f'https://sdmx.oecd.org/public/rest/dataflow/{fin_perstud["agency"]}/{fin_perstud["id"]}/{fin_perstud["version"]}?references=all'

# # Create an instance of the Dataflow class and populate the variables
# df_info = Dataflow(dataflow_details_url)

# print("Populating variables...")
# df_info.populate_variables()
# print("Variables populated.")

# # Flatten the dataflow information for embedding
# flat_info_for_embedding = flatten_info(df_info)

# # Create the document store
# print("Creating the document store...")
# chroma_wrapper = ChromaDBWrapper(flat_info_for_embedding) # should be called with the api key (since i already need it for the LLM)

# def answer_question(user_question):
#     # Get the most similar question and answer from the vector store
#     result_sets = chroma_wrapper.query(user_question, n_results=1)

#     # Generate the answer to the user question
#     persona = """You are a helpful data analyst working for OECD."""
#     prompt = f"""
#     Please provide the answer to the following user question: 
#     {user_question}
#     Please use the information from the source that was selected as the best source to answer the question!
#     This is the most similar question to the user question:
#     '''{result_sets['documents'][0]}'''
    
#     The answer to the question is:
#     '''{result_sets['metadatas'][0][0]['answer']}'''
#     """

#     ans, cost = LLM.model(persona, prompt)
#     return ans

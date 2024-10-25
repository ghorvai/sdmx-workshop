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
        # Re-phrase the user question to improve the semantic search results
        rephrased_question = self._rephrase_user_question(user_question)

        # Get the 3 most relevant entries from the vector store
        result_sets = self.chroma_wrapper.query(rephrased_question, n_results=3)

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
    

    def _rephrase_user_question(self, user_question):
        """
        Before performing the semantic search it is wise to rephrase the user question to improve the search results.
        The idea is to provide consistency in the questions asked instead of having to store all possible ways of asking the same question.
        """

        persona = """You are a helpful data analyst working for OECD."""
        prompt = f"""
        Your task is to rephrase the user question to improve the search results.
        
        Please follow the steps above when rephrasing user questions into a simple and uniform format:
            1. Identify the Core Inquiry: Determine the main point of the question (e.g., dataset name, column presence, code meaning).
            2. Start with a Question Word: Use "What" or "Is" to begin the question.
            3. Focus on the Subject: Clearly state the subject of the question (e.g., dataset, column, code).

        Make sure to:
            - Use Simple Language: Avoid jargon and complex terms.
            - Be Specific: Provide details that help narrow down the search.
        
        In order to further decrease the complexity of the vocabulary used in the user questions, the following rules should be applied:
            - any synonyms to the data source in question (e.g. data, DataFlow, Data Source, Table, Data Set, Data Flow etc.) are replaced with "Table"
            - any synonyms of a Column are replaced with "Column" (e.g. "Variable", "Indicator", "Field", "Attribute", "Measure", "Dimension", "Concept", etc.)
            - any synonyms of Category are replaced with "Category" (e.g. "Code", "Label", "Code Value", etc.). Category is used to refer to the discrete values of a column. 

        Please rephrase the following user question:
        {user_question}
        """

        rephrased_question, cost = LLM.model(persona, prompt)

        return rephrased_question

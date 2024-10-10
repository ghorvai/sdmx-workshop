from openai import OpenAI
import json
import logging
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()

# Instantiate the OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set up logging
logging.basicConfig(filename='llm_interactions.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Global variable to keep track of total price
total_price = 0

# TODO: not all model names are working...
MODEL_PRICING_PER_M_TOKENS = {
    'gpt-4o': {'prompt_tokens': 5.00, 'completion_tokens': 15.00},
    'gpt-4o-2024-08-06': {'prompt_tokens': 2.50, 'completion_tokens': 10.00},
    'gpt-4o-mini': {'prompt_tokens': 0.150, 'completion_tokens': 0.600},
    'gpt-4o-mini-2024-07-18': {'prompt_tokens': 0.150, 'completion_tokens': 0.600},
    'o1-preview': {'prompt_tokens': 15.00, 'completion_tokens': 60.00}
}

def log_interaction(func):
    @wraps(func)
    def wrapper(persona, prompt, model="gpt-4o-mini"):
        global total_price
        
        # Log user message
        logging.info(f"User: {prompt}")
        
        # Call the original function
        message, cost = func(persona, prompt, model)
        
        # Log LLM response and cost
        logging.info(f"LLM: {message}")
        logging.info(f"Cost of this interaction: ${cost:.6f}")
        
        # Update total price
        total_price += cost
        logging.info(f"Total price so far: ${total_price:.6f}")
        
        return message, cost
    return wrapper

@log_interaction
def model(persona, prompt, model="gpt-4o-mini"):
    completion = client.chat.completions.create(
          model=model
        , messages=[
            { "role": "system", "content": persona},
            { "role": "user", "content": prompt}
    ]
        , temperature=0
    )
    # Get the pricing for the model used in the completion
    pricing = MODEL_PRICING_PER_M_TOKENS[completion.model]

    # Calculate the cost of the completion
    prompt_cost = completion.usage.prompt_tokens * pricing['prompt_tokens']
    generation_cost = completion.usage.completion_tokens * pricing['completion_tokens']
    total_cost = (prompt_cost + generation_cost) / 10**6

    # Extract the message from the completion
    message = completion.choices[0].message.content

    return message, total_cost

# Example usage
if __name__ == "__main__":
    persona = "You are a helpful assistant."
    prompt = "What is the capital of France?"
    response, cost = model(persona, prompt)
    print(f"Response: {response}")
    print(f"Cost: ${cost:.6f}")
    print(f"Total cost of all interactions: ${total_price:.6f}")


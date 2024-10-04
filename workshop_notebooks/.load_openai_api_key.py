import json
import os

# Read the JSON file
with open('/Users/ghorvai/Projects/secrets/static_credentials.json') as f:
    secrets = json.load(f)

# Set the API key as an environment variable
if __name__ == '__main__':
    os.environ['OPENAI_API_KEY'] = secrets['openaiKey']
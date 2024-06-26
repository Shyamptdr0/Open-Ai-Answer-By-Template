from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv 
import os
load_dotenv()

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def check_api_key(func):
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key != os.getenv('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return func(*args, **kwargs)
    return wrapper

# Define API endpoint
@app.route('/generate', methods=['POST'])
# @check_api_key
def generate_text():
    data = request.get_json()

    output_parser = StrOutputParser()

    if data is None:
        return jsonify({'error': 'No data provided'})
    
    if 'input' not in data :
        return jsonify({'error': 'Missing input'})

    input_text = data['input']
    # template = data['template']
    template ="You are a intelligent chatbot that responds to quiries based on Indian laws, the Indian Constitution, and the Indian Penal Court."
    llm = ChatOpenAI(model='gpt-3.5-turbo',temperature=0)
    prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("user", "{input}")
    ])

    chain = prompt | llm | output_parser

    # Invoke the LangChain pipeline
    response = chain.invoke({"input": input_text})

    return jsonify({'generated_text': response})

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)

"""Main entry point for the Code Explainer & Refactoring Agent Web UI."""
import os
import logging
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from agents.explainer_agent import ExplainerAgent
from agents.refactoring_agent import RefactoringAgent
from agents.chat_agent import ChatAgent

# --- Initialization ---

# 1. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/agent.log"),
        logging.StreamHandler()
    ]
)

# 2. Load environment variables
load_dotenv()

# 3. Initialize Flask App
app = Flask(__name__)

# 4. Load API Key and Initialize Agents
api_key = os.getenv("GOOGLE_API_KEY")
explainer = None
refactorer = None
chat_agent = None

if not api_key or api_key == "YOUR_API_KEY_HERE":
    logging.error("GOOGLE_API_KEY not found or not set in .env file.")
    # We'll handle this gracefully in the UI/API calls
else:
    try:
        explainer = ExplainerAgent(api_key)
        refactorer = RefactoringAgent(api_key)
        chat_agent = ChatAgent(api_key)
        logging.info("Agents initialized successfully.")
    except Exception as e:
        logging.error(f"Failed to initialize agents: {e}")
        # Agents will remain None

# --- Flask Routes ---

@app.route('/')
def index():
    """Renders the main web page."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """API endpoint to handle code explanation and refactoring."""
    # 1. Check if agents are available
    if not explainer or not refactorer:
        return jsonify({'error': 'Server is not configured correctly. Check API key.'}), 500

    # 2. Get data from the request
    data = request.get_json()
    if not data or 'code' not in data or 'action' not in data:
        return jsonify({'error': 'Invalid request payload.'}), 400

    code = data['code']
    action = data['action']
    
    response_data = {}

    try:
        # 3. Perform the requested action
        logging.info(f"Received action '{action}'")
        
        # Always explain first, getting the structured data
        explanation_data = explainer.explain_code(code)
        response_data['explanation_html'] = explanation_data.get('explanation_html')
        response_data['mermaid_code'] = explanation_data.get('mermaid_code')
        logging.info("Code explanation and diagram generated.")

        # If refactor is requested, also get the refactored code
        if action == 'refactor':
            refactored_code = refactorer.refactor_code(code)
            response_data['refactored_code'] = refactored_code
            logging.info("Code refactoring generated.")
            
        return jsonify(response_data)

    except Exception as e:
        logging.error(f"An error occurred during API call: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_code():
    if not chat_agent:
        return jsonify({'error': 'Server is not configured correctly. Check API key.'}), 500

    data = request.get_json()
    if not data or 'code' not in data or 'query' not in data:
        return jsonify({'error': 'Invalid request: "code" and "query" are required.'}), 400

    try:
        response = chat_agent.get_response(data['code'], data['query'])
        return jsonify({'response': response})
    except Exception as e:
        logging.error(f"An error occurred during /api/chat call: {e}")
        return jsonify({'error': str(e)}), 500


# --- Main Execution ---

if __name__ == '__main__':
    # The 'main' function from the old CLI is no longer needed.
    # We just run the Flask app.
    app.run(debug=True, port=5000)

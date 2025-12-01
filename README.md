# AI Code Helper & Refactoring Agent

This project is a sophisticated, web-based AI assistant that uses the Google Gemini Pro model to analyze, explain, and refactor code. It provides a clean, modern user interface for developers to get insights into their code instantly.

## Description

This agent is designed to act as an AI-powered pair programmer. It helps developers understand complex code and improve its quality by providing:

1.  **Beautiful Explanations:** Instead of plain text, the agent generates a visually appealing breakdown of the code, including a high-level summary and a list of key components, all formatted in easy-to-read HTML.
2.  **Automated Workflow Diagrams:** The agent automatically generates a flowchart of the code's logic using Mermaid.js, providing a clear visual representation of how the code works.
3.  **Intelligent Refactoring:** The agent can rewrite code to improve its readability, performance, and adherence to modern best practices.

This project demonstrates several key concepts, including:
-   **Multi-agent System:** A Flask backend orchestrates a sequential pipeline between an `ExplainerAgent` and a `RefactoringAgent`.
-   **Context Engineering:** Both agents use highly-engineered prompts to instruct the LLM to return structured data (HTML, Mermaid.js syntax, JSON).
-   **Observability:** All agent activities are logged for easy debugging and monitoring.
-   **Agent Deployment:** The agent is deployed as a user-friendly web application using the Flask framework.

## How to Use

1.  **Prerequisites:**
    -   Python 3.9+
    -   A Google Gemini API key.

2.  **Setup:**
    -   Clone this repository.
    -   Install the required dependencies from `requirements.txt`:
        ```bash
        pip install -r requirements.txt
        ```
    -   Create a `.env` file in the root of the project by copying the `.env.example` or creating it manually.
    -   Add your Gemini API key to the `.env` file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

3.  **Run the Application:**
    -   Execute the `main.py` script to start the web server:
        ```bash
        python main.py
        ```
    -   Open your web browser and navigate to:
        ```
        http://127.0.0.1:5000
        ```
    -   Paste your code into the text area or upload a file to begin.

## Project Structure

```
.
├── agents/
│   ├── explainer_agent.py
│   └── refactoring_agent.py
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   └── index.html
├── logs/
│   └── agent.log
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

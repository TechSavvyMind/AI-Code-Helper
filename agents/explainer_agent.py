"""Agent responsible for explaining code."""
import google.generativeai as genai

"""Agent responsible for explaining code."""
import google.generativeai as genai
import re
import json

class ExplainerAgent:
    """
    This agent uses a generative model to explain a given piece of code,
    generating both an HTML explanation and a Mermaid.js diagram.
    """
    def __init__(self, api_key):
        """Initializes the ExplainerAgent."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def _parse_json_from_response(self, text):
        """More robustly parses JSON from the model's text response."""
        try:
            # First, try to load the whole text as JSON
            return json.loads(text)
        except json.JSONDecodeError:
            # If that fails, find the JSON block using regex
            match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    return None
        return None

    def explain_code(self, code_content, language="python"):
        """
        Explains a piece of code and generates a workflow diagram.

        Args:
            code_content (str): The code to explain.
            language (str): The programming language of the code.

        Returns:
            dict: A dictionary containing 'explanation_html' and 'mermaid_code'.
        """
        prompt = f"""
        You are an expert software documentation writer. Analyze the following {language} code and provide a two-part explanation.

        **Part 1: HTML Explanation**
        Generate a concise, easy-to-read HTML snippet that explains the code. Structure it as follows:
        - Use an `<h4>` tag for a "High-Level Summary".
        - Use a `<p>` tag for a brief summary.
        - Use an `<h4>` tag for "Key Components".
        - Use a `<ul>` with `<li>` items for each function, class, or key part. Inside each `<li>`, use `<strong>` for the name and follow it with a short description.
        - Do NOT include `<html>` or `<body>` tags.

        **Part 2: Mermaid.js Flowchart**
        Generate a Mermaid.js flowchart definition that illustrates the code's workflow.
        - The flowchart should be a `graph TD` (Top-Down).
        - Use clear, short labels for nodes.
        - Example: `A[Start] --> B(Process Data) --> C{{Decision}} --> D[End]`.

        **Your final output must be a single, valid JSON object** with two keys: "explanation_html" and "mermaid_code", wrapped in a ```json markdown block.

        **Code to analyze:**
        ```python
        {code_content}
        ```
        """
        try:
            response = self.model.generate_content(prompt)
            response_json = self._parse_json_from_response(response.text)

            if response_json:
                return {
                    "explanation_html": response_json.get("explanation_html", "<p>Error: Explanation format is invalid.</p>"),
                    "mermaid_code": response_json.get("mermaid_code", "graph TD; error[Invalid diagram format];")
                }
            else:
                 raise ValueError("Failed to parse JSON from model response.")

        except Exception as e:
            # Fallback for any errors during generation or parsing
            error_message = f"An error occurred during code explanation: {str(e)}"
            return {
                "explanation_html": f"<p>{error_message}</p>",
                "mermaid_code": "graph TD; error[An error occurred];"
            }


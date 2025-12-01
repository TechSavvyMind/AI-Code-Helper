"""Agent responsible for refactoring code."""
import google.generativeai as genai

class RefactoringAgent:
    """
    This agent uses a generative model to suggest and apply refactorings to code.
    """
    def __init__(self, api_key):
        """
        Initializes the RefactoringAgent.

        Args:
            api_key (str): The API key for the generative model.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def refactor_code(self, code_content, language="python", instructions=""):
        """
        Suggests refactorings for a piece of code.

        Args:
            code_content (str): The code to refactor.
            language (str): The programming language of the code.
            instructions (str): Optional user instructions for refactoring.

        Returns:
            str: The refactored code, enclosed in a markdown code block.
        """
        prompt = f"""
        As an expert software engineer specializing in code quality and maintainability, please refactor the following {language} code.

        **Refactoring Goals:**
        - Improve readability and clarity.
        - Enhance performance where applicable.
        - Adhere to idiomatic {language} best practices.
        - Add docstrings and type hints if they are missing.
        - Simplify complex logic.

        {f"**User Instructions:** {instructions}" if instructions else ""}

        Return ONLY the complete, refactored code in a single markdown block. Do not include explanations or apologies in your response.

        **Original Code:**
        ```python
        {code_content}
        ```
        """
        try:
            # Create a generation config to get raw text
            generation_config = genai.types.GenerationConfig(
                candidate_count=1,
                # Force the model to generate text
                response_mime_type="text/plain",
            )
            response = self.model.generate_content(prompt, generation_config=generation_config)

            # Clean up the response to get only the code
            refactored_code = response.text.strip()
            if refactored_code.startswith("```python"):
                refactored_code = refactored_code[len("```python"):].strip()
            if refactored_code.endswith("```"):
                refactored_code = refactored_code[:-len("```")].strip()

            return refactored_code
        except Exception as e:
            return f"An error occurred during code refactoring: {e}"

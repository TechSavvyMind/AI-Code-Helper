from langchain_google_genai import ChatGoogleGenerativeAI
import os

class ChatAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

    def get_response(self, code, query):
        if not query:
            return "Please ask a question about the code."

        prompt = f"""
        You are an expert programmer and a helpful code assistant.
        A user has a question about the following code. Please provide a clear and concise answer.

        Code:
        ```
        {code}
        ```

        User's Question: {query}

        Your Answer:
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"An error occurred: {e}"
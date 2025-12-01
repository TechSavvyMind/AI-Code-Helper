document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const codeInput = document.getElementById('code-input');
    const explainBtn = document.getElementById('explain-btn');
    const refactorBtn = document.getElementById('refactor-btn');
    const copyBtn = document.getElementById('copy-btn');

    const loader = document.getElementById('loader');
    const explanationContainer = document.getElementById('explanation-container');
    const explanationOutput = document.getElementById('explanation-output');
    const diagramOutput = document.getElementById('diagram-output');
    const refactorContainer = document.getElementById('refactor-container');
    const refactorOutput = document.getElementById('refactor-output');

    // --- Chat Elements ---
    const chatMessages = document.getElementById('chat-messages');
    const chatInput = document.getElementById('chat-input');
    const sendChatBtn = document.getElementById('send-chat-btn');

    // Trigger file input
    uploadBtn.addEventListener('click', () => fileInput.click());

    // Read file content
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) => {
            codeInput.value = e.target.result;
        };
        reader.readAsText(file);
    });

    // Handle button clicks
    explainBtn.addEventListener('click', () => handleApiRequest('explain'));
    refactorBtn.addEventListener('click', () => handleApiRequest('refactor'));
    
    // Handle copy button click
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(refactorOutput.textContent).then(() => {
            copyBtn.textContent = 'Copied!';
            setTimeout(() => { copyBtn.textContent = 'Copy Code'; }, 2000);
        });
    });

    // --- Chat Functionality ---
    sendChatBtn.addEventListener('click', handleChatSubmit);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleChatSubmit();
        }
    });

    async function handleChatSubmit() {
        const query = chatInput.value.trim();
        const code = codeInput.value;

        if (!query) return;
        if (!code.trim()) {
            alert('Please enter some code in the main editor to ask questions about it.');
            return;
        }

        addMessage(query, 'user');
        chatInput.value = '';
        chatInput.placeholder = 'Ask a follow-up question...';
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, query }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown server error occurred');
            }

            const data = await response.json();
            addMessage(data.response, 'ai');

        } catch (error) {
            addMessage(`Error: ${error.message}`, 'ai');
        }
    }

    function addMessage(text, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', `${sender}-message`);
        if (sender === 'ai') {
            messageElement.innerHTML = parseMarkdown(text);
        } else {
            messageElement.textContent = text;
        }
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
    }

    function parseMarkdown(markdownText) {
        let htmlText = markdownText;
        // Convert bold text (e.g., **bold**)
        htmlText = htmlText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Convert newlines to <br/>
        htmlText = htmlText.replace(/\n/g, '<br/>');
        return htmlText;
    }


    async function handleApiRequest(action) {
        const code = codeInput.value;
        if (!code.trim()) {
            alert('Please enter or upload some code.');
            return;
        }

        // Reset UI
        loader.style.display = 'block';
        explanationContainer.style.display = 'none';
        refactorContainer.style.display = 'none';
        explanationOutput.innerHTML = '';
        diagramOutput.innerHTML = '';
        refactorOutput.textContent = '';

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code, action }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'An unknown server error occurred');
            }

            const data = await response.json();
            
            // Display structured HTML explanation
            if (data.explanation_html) {
                explanationOutput.innerHTML = data.explanation_html;
                explanationContainer.style.display = 'flex';
            }
            
            // Validate and render the Mermaid diagram
            if (data.mermaid_code) {
                try {
                    // First, validate the syntax without rendering
                    await window.mermaid.parse(data.mermaid_code);
                    
                    // If valid, inject and render
                    diagramOutput.innerHTML = `<pre class="mermaid">${data.mermaid_code}</pre>`;
                    await window.mermaid.run({
                        nodes: document.querySelectorAll('.mermaid'),
                    });
                } catch (e) {
                    // If syntax is invalid, show a friendly error
                    console.error("Mermaid syntax error:", e);
                    diagramOutput.innerHTML = `<div class="error-box">Could not generate a valid workflow diagram. The AI model provided invalid syntax.</div>`;
                }
            }

            // Display refactored code
            if (data.refactored_code) {
                refactorOutput.textContent = data.refactored_code;
                refactorContainer.style.display = 'flex';
            }

        } catch (error) {
            alert(`An error occurred: ${error.message}`);
        } finally {
            loader.style.display = 'none';
        }
    }
});
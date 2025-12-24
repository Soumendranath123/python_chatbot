import datetime
from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)

# ------------------------------------------------------------------
# HTML, CSS, and JavaScript Frontend
# ------------------------------------------------------------------
# We store this in a string to keep the example in a single file.
# In a larger project, you would save this as 'templates/index.html'.
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Chatbot</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .chat-container {
            width: 400px;
            max-width: 90%;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            display: flex;
            flex-direction: column;
            height: 80vh;
        }
        .chat-header {
            background-color: #0084ff;
            color: white;
            padding: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.2rem;
        }
        .chat-box {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background-color: #fff;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .message {
            max-width: 80%;
            padding: 10px 15px;
            border-radius: 18px;
            font-size: 0.95rem;
            line-height: 1.4;
            position: relative;
            word-wrap: break-word;
        }
        .bot-message {
            background-color: #e4e6eb;
            color: black;
            align-self: flex-start;
            border-bottom-left-radius: 2px;
        }
        .user-message {
            background-color: #0084ff;
            color: white;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }
        .input-area {
            display: flex;
            padding: 15px;
            border-top: 1px solid #ddd;
            background-color: #f9f9f9;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #0084ff;
        }
        button {
            background-color: #0084ff;
            color: white;
            border: none;
            padding: 10px 20px;
            margin-left: 10px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: bold;
            transition: background-color 0.2s;
        }
        button:hover {
            background-color: #006bcf;
        }
        /* Scrollbar styling */
        .chat-box::-webkit-scrollbar {
            width: 6px;
        }
        .chat-box::-webkit-scrollbar-thumb {
            background-color: rgba(0,0,0,0.2);
            border-radius: 3px;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">
        Simple Bot
    </div>
    <div class="chat-box" id="chat-box">
        <!-- Messages will appear here -->
        <div class="message bot-message">Hello! I'm a Python bot. Ask me anything.</div>
    </div>
    <div class="input-area">
        <input type="text" id="user-input" placeholder="Type a message..." onkeypress="handleKeyPress(event)">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // 1. Add User Message to Chat
        addMessage(text, 'user-message');
        userInput.value = '';

        // 2. Send to Python Backend
        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            
            // 3. Add Bot Response to Chat
            addMessage(data.response, 'bot-message');

        } catch (error) {
            console.error('Error:', error);
            addMessage("Sorry, I'm having trouble connecting to the server.", 'bot-message');
        }
    }

    function addMessage(text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>

</body>
</html>
"""

# ------------------------------------------------------------------
# Backend Logic
# ------------------------------------------------------------------

def get_bot_response(user_text):
    """
    Simple rule-based logic for the chatbot.
    You can replace this with AI, database lookups, etc.
    """
    text = user_text.lower()
    
    if "hello" in text or "hi" in text or "hey" in text :
        return random.choice(["Hello there!", "Hi! How can I help?", "Greetings!"])
    
    elif "how are you" in text:
        return "I'm just a computer program, but I'm running perfectly! How are you?"
    
    elif "time" in text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    
    elif "name" in text:
        return "I am a simple Python Chatbot created by Soumendra."
    
    elif "bye" in text or "goodbye" in text:
        return "Goodbye! Have a great day!"
        
    else:
        return "I'm not sure I understand. Try asking about the time or just say hello!"

# ------------------------------------------------------------------
# Flask Routes
# ------------------------------------------------------------------

@app.route('/')
def home():
    """Serves the HTML frontend"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_response', methods=['POST'])
def chat():
    """Handles JSON requests from the frontend"""
    data = request.get_json()
    user_message = data.get('message', '')
    
    bot_reply = get_bot_response(user_message)
    
    return jsonify({'response': bot_reply})

if __name__ == '__main__':
    print("Starting Chatbot on http://127.0.0.1:5000")
    app.run(debug=True)
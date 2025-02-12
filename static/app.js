class Chatbox {
    constructor() {
        this.args = {
            chatBox: document.querySelector('.chat-container'),
            sendButton: document.querySelector('.submit_button'),
            textField: document.querySelector('.chat-container input'),
            chatMessagesContainer: document.querySelector('.window_messages')
        };
        this.state = false;
        this.messages = [];
    }

    display() {
        this.setupEventListeners();
        if (window.location.pathname === "/chat") {
            this.addMessage('Antidote', "Salut ! Je suis Antidote, ton guide de la survie en cas de blessures ou d'empoisonnement.");
                    this.updateChatText();
                }
    }

    setupEventListeners() {
        const { sendButton, textField, chatBox } = this.args;

        sendButton.addEventListener('click', () => this.onSendButton(chatBox));
        textField.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    onSendButton(chatBox) {
        const textField = this.args.textField;
        const messageText = textField.value.trim();

        if (!messageText) return;

        this.addMessage('User', messageText);
        textField.value = '';

        this.updateChatText(chatBox);

        this.sendMessageToBot(messageText)
            .then(response => {
                this.addMessage('Antidote', response.answer);
                this.updateChatText(chatBox);
            })
            .catch(error => {
                console.error('Error:', error);
                this.addMessage('Antidote', "Je n'ai pas pu te trouver cette information !");
                this.updateChatText(chatBox);
            });
    }

    addMessage(sender, messageText) {
        this.messages.push({ name: sender, message: messageText });
    }

    sendMessageToBot(messageText) {
        return fetch('/generate', {
            method: 'POST',
            body: JSON.stringify({ message: messageText }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json());
    }

    updateChatText(chatbox) {
        const messagesHtml = this.messages.slice().reverse().map(({ name, message }) => {
            const messageClass = name === "Antidote" ? "messages_content--visitor" : "messages_content--operator";
            return `<div class="messages_content ${messageClass}">${message}</div>`;
        }).join('');

        this.args.chatMessagesContainer.innerHTML = messagesHtml;
    }

    askQuestion() {
        let question = document.getElementById("query").value;
        
        fetch("http://127.0.0.1:5000/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: question })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("response").innerText = data.response;
        })
        .catch(error => console.error("Error:", error));
    }
    
}

const chatbox = new Chatbox();
chatbox.display();
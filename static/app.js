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
        console.log("La fonction display() s'exécute !");
        this.setupEventListeners();
        if (window.location.pathname === "/chat") {
            console.log("Ajout du message de bienvenue...");
            this.addMessage('Antidote', `Salut ${username} ! Je suis Antidote, ton guide de la survie en cas de blessures ou d'empoisonnement.`);
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
    
        // Afficher l'effet de frappe
        this.showTypingIndicator();
    
        setTimeout(() => {
            this.sendMessageToBot(messageText)
                .then(response => {
                    this.removeTypingIndicator(); // Supprimer l'animation de frappe
                    this.addMessage('Antidote', response.answer);
                    this.updateChatText(chatBox);
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.removeTypingIndicator();
                    this.addMessage('Antidote', "Je n'ai pas pu te trouver cette information !");
                    this.updateChatText(chatBox);
                });
        }, 1500); // Simulation d'un délai avant la réponse du bot
    }


    showTypingIndicator() {
        this.addMessage('Antidote', `<span class="typing-indicator">Antidote est en train d'écrire...</span>`);
        this.updateChatText();
    }
    
    
    removeTypingIndicator() {
        this.messages = this.messages.filter(msg => !msg.message.includes("Antidote est en train d'écrire"));
        this.updateChatText();
    }
    
    

    addMessage(sender, messageText) {
        
        this.messages.push({ name: sender, message: messageText });
        console.log(`Ajout du message : ${sender} - ${messageText}`); // DEBUG
        console.log("Valeur de username :", username);
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
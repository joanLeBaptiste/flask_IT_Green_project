
// SCRIPT RESERVE POURLE CHATBOT
function sendMessage() {
    var userInput = document.getElementById("user-input").value.trim();
    if (!userInput) return;

    var chatLog = document.getElementById("chat-log");
    chatLog.innerHTML += "<p><strong>User:</strong> " + userInput + "</p>";
    document.getElementById("user-input").value = "";

    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const botMessage = data.response || data.error || "No response";
        chatLog.innerHTML += "<p><strong>Chatbot:</strong> " + botMessage + "</p>";
        chatLog.scrollTop = chatLog.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        chatLog.innerHTML += "<p><strong>Chatbot:</strong> Erreur de connexion.</p>";
    });
}

function toggleChat() {
    var chatContainer = document.getElementById("chat-container");
    var toggleButton = document.getElementById("toggle-chat");
    if (chatContainer.style.display === "none" || chatContainer.style.display === "") {
        chatContainer.style.display = "flex";
        toggleButton.textContent = "-";
    } else {
        chatContainer.style.display = "none";
        toggleButton.textContent = "💬";
    }
}

function resetChat() {
    // Efface le chat log côté client
    const chatLog = document.getElementById('chat-log');
    chatLog.innerHTML = "";

    // Efface aussi le contexte côté serveur
    fetch("/chatbot/reset", {
        method: "POST"
    }).then(() => {
        chatLog.innerHTML += `<p class="bot-message"><em>Le chatbot a été réinitialisé.</em></p>`;
    });
}

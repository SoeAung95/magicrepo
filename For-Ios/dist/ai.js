// AI Chatbot Frontend Handler - Enhanced with null checks
const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");

async function sendMessage() {
    if (!userInput) return;
    const message = userInput.value.trim();
    if (!message) return;

    // Display user message
    if (chatBox) {
        chatBox.innerHTML += `<div class="msg user">${message}</div>`;
        userInput.value = "";

        try {
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: message })
            });

            const data = await res.json();
            chatBox.innerHTML += `<div class="msg bot">${data.reply}</div>`;
        } catch (err) {
            chatBox.innerHTML += `<div class="msg error">❌ Error: ${err.message}</div>`;
        }

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

// Only add event listeners if elements exist
if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
}

if (userInput) {
    userInput.addEventListener("keypress", e => {
        if (e.key === "Enter") sendMessage();
    });
}

// Console log for debugging
console.log('AI.js loaded - Elements found:', {
    chatBox: !!chatBox,
    userInput: !!userInput,
    sendBtn: !!sendBtn
});}
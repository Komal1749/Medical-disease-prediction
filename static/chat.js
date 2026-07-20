const chatBtn = document.getElementById("chatbot-btn");
const chatbot = document.getElementById("chatbot");
const closeChat = document.getElementById("close-chat");
const chatBox = document.getElementById("chat-body");
const input = document.getElementById("userMessage");

// Open chatbot
chatBtn.addEventListener("click", () => {
    chatbot.style.display = "block";
});

// Close chatbot
closeChat.addEventListener("click", () => {
    chatbot.style.display = "none";
});

// Send message
function sendMessage() {

    let message = input.value.trim();

    if(message === "") return;

    chatBox.innerHTML += `
        <div class="user">
            ${message}
        </div>
    `;

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: "message=" + encodeURIComponent(message)
    })
    .then(res => res.json())
    .then(data => {

        chatBox.innerHTML += `
            <div class="bot">
                ${data.reply}
            </div>
        `;

        input.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        chatBox.innerHTML += `
            <div class="bot">
                Error: Could not connect to AI.
            </div>
        `;
        console.error(error);
    });
}

// Press Enter to send
input.addEventListener("keypress", function(event){
    if(event.key === "Enter"){
        event.preventDefault();
        sendMessage();
    }
});
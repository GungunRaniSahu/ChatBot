function appendMessage(content, sender, time = "") {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.classList.add("message", sender);
    div.innerHTML = `<strong>${sender === 'user' ? 'You' : 'Bot'}:</strong> ${content}
      <div class="time">${time}</div>`;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
  }
  
  function sendMessage() {
    const userInput = document.getElementById("userInput");
    const message = userInput.value.trim();
    if (message === "") return;
  
    appendMessage(message, "user");
  
    appendMessage("Typing...", "bot");
  
    fetch("/get", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: message })
    })
      .then(res => res.json())
      .then(data => {
        const botMessages = document.querySelectorAll(".bot");
        const lastBotMessage = botMessages[botMessages.length - 1];
        if (lastBotMessage && lastBotMessage.textContent.includes("Typing...")) {
          lastBotMessage.remove(); 
        }
        appendMessage(data.response, "bot", data.time);
      });
  
    userInput.value = "";
  }
  
  
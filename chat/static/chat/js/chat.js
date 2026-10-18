const chatHistory = document.getElementById("chatHistory");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const errorBanner = document.getElementById("errorBanner");
const errorMessage = document.getElementById("errorMessage");

function scrollToBottom() {
  chatHistory.scrollTo({
    top: chatHistory.scrollHeight,
    behavior: "smooth"
  });
}

function showError(msg) {
  errorMessage.innerText = msg;
  errorBanner.classList.remove("hidden");
}

function dismissError() {
  errorBanner.classList.add("hidden");
}

function sendQuickPrompt(promptText) {
  userInput.value = promptText;
  handleSend(new Event("submit"));
}

function clearHistory() {
  chatHistory.innerHTML = `
    <div class="flex items-start gap-2.5">
      <div class="w-7 h-7 rounded-full bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center text-cyan-300 text-xs flex-shrink-0 shadow-[0_0_12px_rgba(6,182,212,0.4)]">
        🤖
      </div>
      <div class="bg-cyan-500 text-slate-950 font-medium rounded-2xl rounded-tl-sm p-3 max-w-[85%] shadow-[0_0_20px_rgba(6,182,212,0.3)] text-xs leading-relaxed speech-tail-left">
        <div class="flex items-center gap-2 mb-1">
          <span class="font-bold text-black tracking-wide">Session Reset ⚡</span>
          <span class="bg-slate-950 text-cyan-300 text-[9px] px-1.5 py-0.5 rounded font-mono font-bold tracking-wider">READY</span>
        </div>
        <p>Chat history has been cleared successfully. How can I assist you with Big Brains today?</p>
        <span class="text-[9px] text-slate-800 font-semibold mt-1.5 block">Just now</span>
      </div>
    </div>
  `;
  dismissError();
}

async function handleSend(e) {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;

  dismissError();

  // User Message (Right Side)
  const userBubble = `
    <div class="flex items-start justify-end gap-2.5">
      <div class="bg-slate-800 border border-white/10 text-white rounded-2xl rounded-tr-sm p-3.5 max-w-[85%] text-xs shadow-md leading-relaxed">
        <p>${message}</p>
      </div>
    </div>
  `;
  chatHistory.insertAdjacentHTML("beforeend", userBubble);
  userInput.value = "";
  scrollToBottom();

  // Loading State Indicator (Robot Avatar 🤖)
  userInput.disabled = true;
  sendBtn.disabled = true;

  const loadingId = "loader-" + Date.now();
  const loadingBubble = `
    <div id="${loadingId}" class="flex items-start gap-2.5">
      <div class="w-7 h-7 rounded-full bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center text-cyan-300 text-xs flex-shrink-0 shadow-[0_0_12px_rgba(6,182,212,0.4)]">
        🤖
      </div>
      <div class="bg-cyan-500/90 text-slate-950 rounded-2xl rounded-tl-sm px-4 py-3 shadow-[0_0_15px_rgba(6,182,212,0.3)] flex items-center gap-1.5 speech-tail-left">
        <span class="w-2 h-2 rounded-full bg-slate-950 animate-bounce"></span>
        <span class="w-2 h-2 rounded-full bg-slate-950 animate-bounce [animation-delay:0.2s]"></span>
        <span class="w-2 h-2 rounded-full bg-slate-950 animate-bounce [animation-delay:0.4s]"></span>
      </div>
    </div>
  `;
  chatHistory.insertAdjacentHTML("beforeend", loadingBubble);
  scrollToBottom();

  try {
    const res = await fetch("/api/ask/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message })
    });

    const data = await res.json();
    const loader = document.getElementById(loadingId);
    if (loader) loader.remove();

    if (res.ok && data.status === "success") {
      // AI Reply Bubble (Robot Avatar 🤖)
      const aiBubble = `
        <div class="flex items-start gap-2.5">
          <div class="w-7 h-7 rounded-full bg-cyan-500/20 border border-cyan-400/40 flex items-center justify-center text-cyan-300 text-xs flex-shrink-0 shadow-[0_0_12px_rgba(6,182,212,0.4)]">
            🤖
          </div>
          <div class="bg-cyan-500 text-slate-950 font-medium rounded-2xl rounded-tl-sm p-3.5 max-w-[85%] shadow-[0_0_20px_rgba(6,182,212,0.3)] text-xs leading-relaxed speech-tail-left">
            <p>${data.reply}</p>
          </div>
        </div>
      `;
      chatHistory.insertAdjacentHTML("beforeend", aiBubble);
    } else {
      showError(data.error || "Failed to receive response from server.");
    }
  } catch (err) {
    const loader = document.getElementById(loadingId);
    if (loader) loader.remove();
    showError("Network error: Server is unreachable.");
  } finally {
    userInput.disabled = false;
    sendBtn.disabled = false;
    userInput.focus();
    scrollToBottom();
  }
}
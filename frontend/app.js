/**
 * Kara - Tuana's Personal Chatbot Logic
 * Theme: Sarcastic, B12-Deficient, but Helpful
 */

const chat = document.getElementById("chat");
const input = document.getElementById("input");
const sendBtn = document.getElementById("send");
const avatar = document.getElementById("avatar-container");

// Unique session ID for the backend to track context
const SESSION_ID = "sess_" + crypto.randomUUID();

// --- 1. Sarcastic B12 Comment Generator ---
const getB12Quip = () => {
  const quips = [
    "Searching my memory... if I still have one...",
    "Brain cells are loading... slowly...",
    "Trying to focus, but the fog is real today.",
    "Processing... (This would be faster if Tuana fed me vitamins)",
    "Consulting my last remaining B12 molecule...",
    "Wait, what was the question? Just kidding, searching...",
    "One second, my synapses are buffering...",
    "Calculating... please don't use big words, it hurts...",
    "Tuana told me this once... I think..."
  ];
  return quips[Math.floor(Math.random() * quips.length)];
};

// --- 2. Dynamic Time Greeting ---
function getGreeting() {
  const hour = new Date().getHours();
  let timeOfDay = "Good evening! 🌙";
  
  if (hour < 12) timeOfDay = "Good morning! ☀️";
  else if (hour < 18) timeOfDay = "Good afternoon! ☕";
  
  return `${timeOfDay} I'm Kara. I’d tell you everything about Tuana, but I forgot why I walked into this browser window. 🩷 Ask me something before I lose my train of thought!`;
}

// --- 3. Initialize Chat ---
window.addEventListener('DOMContentLoaded', () => {
  // Clear chat except for the first message if needed, then add greeting
  addMessage(getGreeting(), "bot");
});

// --- 4. Message UI Helper ---
function addMessage(text, role) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  chat.appendChild(div);
  
  // Smooth scroll to bottom
  chat.scrollTo({
    top: chat.scrollHeight,
    behavior: 'smooth'
  });
  
  return div;
}

// --- 5. Main Send Function ---
async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;

  // Add user message to UI
  addMessage(text, "user");
  input.value = "";

  // Visual "Thinking" feedback
  avatar.classList.add("thinking");
  
  const typingIndicator = document.createElement("div");
  typingIndicator.className = "message bot";
  typingIndicator.style.fontStyle = "italic";
  typingIndicator.style.opacity = "0.7";
  typingIndicator.textContent = getB12Quip();
  chat.appendChild(typingIndicator);
  chat.scrollTop = chat.scrollHeight;

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        question: text,
        session_id: SESSION_ID
      })
    });

    if (!res.ok) throw new Error("API Glitch");

    const data = await res.json();
    typingIndicator.remove();

    // The "Forgetful" Quirk: 5% chance she just blanks out
    if (Math.random() < 0.05) {
      addMessage("I actually had a great answer for that, but it vanished into the fog. Try asking again? It's the B12, I swear.", "bot");
    } else {
      addMessage(data.answer || "My brain just hit a 404. Too much fog, not enough vitamins.", "bot");
    }

  } catch (e) {
    typingIndicator.remove();
    addMessage("Error. My neural circuits just took a nap. I blame the deficiency.", "bot");
    console.error("Chat Error:", e);
  } finally {
    // Stop the avatar pulse
    avatar.classList.remove("thinking");
  }
}

// --- 6. Event Listeners ---
sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", e => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
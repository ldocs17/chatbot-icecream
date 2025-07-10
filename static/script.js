const toggleButton = document.getElementById('chatbot-toggle');
const chatbotWindow = document.getElementById('chatbot-window');
const messagesContainer = document.getElementById('chatbot-messages');
const bookingForm = document.getElementById('booking-form');

toggleButton.addEventListener('click', () => {
  chatbotWindow.style.display = chatbotWindow.style.display === 'none' ? 'flex' : 'none';
});

async function sendMessage() {
  const input = document.getElementById('user-message');
  const userMessage = input.value.trim();
  if (!userMessage) return;

  appendMessage('You', userMessage);
  input.value = '';

  if (userMessage.toLowerCase().includes("book")) {
    bookingForm.style.display = 'block';
    return;
  }

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage })
    });
    const data = await res.json();
    appendMessage('Bot', data.reply);
  } catch (err) {
    appendMessage('Bot', 'Sorry, something went wrong.');
  }
}

function appendMessage(sender, message) {
  const msg = document.createElement('div');
  msg.textContent = `${sender}: ${message}`;
  messagesContainer.appendChild(msg);
  messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function submitBooking() {
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const date = document.getElementById('date').value;
  const details = document.getElementById('details').value;

  if (!name || !email || !date || !details) {
    alert("Please fill out all fields.");
    return;
  }

  console.log("Booking submitted:", { name, email, date, details });
  appendMessage('Bot', `Thanks ${name}, your event on ${date} has been received. We'll contact you at ${email}!`);
  bookingForm.style.display = 'none';
}

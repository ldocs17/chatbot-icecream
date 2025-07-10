from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

store_knowledge = """Scoops – The Chatham Creamery is open daily from 12 PM to 10 PM. They are located at 228 Main St, Chatham, NJ 07928, phone (973) 507-9223.
Popular flavors include Mint Chocolate Chip, Campfire S’mores, Moose Tracks, Chocolate Lover's, Sea Salt Caramel, and Peanut Butter Pie. Vegan oat-based flavors include mint cookie, raspberry chip, and chocolate.
Pricing:
- 1 scoop: $6.50
- 2 scoops: $7.95
- Soft serve: $3.25
- Sundaes/milkshakes: $6.99–$8.50
Scoops Bus Packages:
- Bus Stop (30 mins / 30 servings): $249
- Brain Freeze (1 hr / 60 servings): $449
- Ice Cream Social (1.5 hr / 90 servings): $599
They serve Gifford’s ice cream imported from Maine and often host fundraisers like the Peppermint Palooza supporting local PTO events."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "")

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a friendly assistant for a local ice cream shop. Answer based only on the information provided below."},
                {"role": "user", "content": f"{store_knowledge}\n\nQuestion: {user_msg}"}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({ "reply": reply })

    except openai.OpenAIError as e:
        print("OpenAI error:", e)
        fallback_response = get_fallback_response(user_msg)
        return jsonify({ "reply": fallback_response }), 200
    except Exception as e:
        print("Server error:", e)
        return jsonify({ "reply": "Sorry, something went wrong." }), 500

def get_fallback_response(message):
    message_lower = message.lower()
    if "open" in message_lower or "hours" in message_lower:
        return "We're open every day from 12 PM to 10 PM!"
    elif "pie" in message_lower:
        return "Our ice cream pies start at $19.95 depending on the flavor."
    elif "book" in message_lower or "bus" in message_lower:
        return "You can book our Ice Cream Bus starting at $249! Let me know the event details."
    else:
        return "I'm currently offline, but feel free to ask about hours, booking, or pricing!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

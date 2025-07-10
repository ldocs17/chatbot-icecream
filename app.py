from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "YOUR_OPENAI_API_KEY"

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
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a friendly assistant for a local ice cream shop. Answer based only on the information provided below."},
                {"role": "user", "content": f"{store_knowledge}\n\nQuestion: {user_msg}"}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Sorry, something went wrong. ({e})"}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

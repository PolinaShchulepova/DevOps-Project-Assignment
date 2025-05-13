from flask import Flask, request, jsonify, render_template
import redis
import random
import os

app = Flask(__name__)
r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'),port=6379, decode_responses=True)


@app.route('/quote')
def get_quote():
    quotes = r.lrange("quotes", 0, -1) 
    if not quotes:
        return "No quotes available yet"
    return random.choice(quotes)

@app.route('/form')
def show_form():
    return render_template("add_quote.html")

@app.route('/add-quote', methods=['POST'])
def add_quote():
    data = request.get_json()
    quote = data.get('quote')

    if not quote:
        return jsonify({'error': 'No quote provided'}), 400 

  r.rpush("quotes", quote) 
    return jsonify({'message': 'Quote added successfully!'}), 201  

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


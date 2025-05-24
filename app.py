from flask import Flask, request, jsonify, render_template
import redis
import random
import os

app = Flask(__name__)
r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, decode_responses=True)  # Use meaningful names for variables, r can be redis_client

@app.route('/quote')
def get_quote():
    quotes = r.lrange("quotes", 0, -1)
    if not quotes: # add blank line before if statement for better readability
        return render_template("quote.html", quote="No quotes available yet")
    random_quote = random.choice(quotes) # add blank line after if statement for better readability
    return render_template("quote.html", quote=random_quote) # add blank line before return statement for better readability

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
    return jsonify({'message': 'Quote added successfully!'}), 201 # add a blank line before the return statement for better readability


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
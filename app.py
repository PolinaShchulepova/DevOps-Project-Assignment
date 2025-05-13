from flask import Flask, request 
import redis
import random

app = Flask(__name__)
r = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'),port=6379, decode_responses=True)


@app.route('/quote')
def get_quote():
    quotes = r.lrange("quotes", 0, -1) 
    if not quotes:
        return "No quotes available yet"
    return random.choice(quotes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
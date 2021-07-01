from flask import Flask
from flask import request
import genius
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/lyrics', methods=['POST'])
def get_lyrics():
    incoming_msg = request.values.get('Body', '').lower()
    if incoming_msg.startswith('nickname'):
        result = genius.set_nickname(incoming_msg)
    elif incoming_msg.startswith('list'):
        result = genius.examples(incoming_msg)
    else:
        result = genius.get_lyrics(incoming_msg)
    resp = MessagingResponse()
    msg = resp.message(result)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)

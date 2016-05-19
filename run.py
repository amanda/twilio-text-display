from flask import Flask, request, render_template
import os
import psycopg2
import urlparse
import cgi

app = Flask(__name__)

# global postgres stuff
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cur = conn.cursor()

@app.route("/", methods=['POST'])
def get_text_body():
    """route that the twilio api POSTs to with text messages"""
    body = request.values.get('Body', None)
    print body
    # write message to the DB
    try:
        cur.execute("INSERT INTO bigf.texts (message) VALUES (%s)", [body])
    except Exception as e:
        print e
    return str(body)

@app.route("/raw", methods=['GET'])
def get_raw_file():
    """route to get raw text for sending to the voicebox"""
    pass

@app.route("/messages", methods=['GET'])
def get_messages():
    """route to display messages in a pretty way for the audience"""
    pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
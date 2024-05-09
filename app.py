import app
from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from chat import get_response

import logging
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
app.secret_key = 'happy_song_12'
authenticated_users = set()
# Dummy user data (replace with a proper user database)
users = {
    "user1": "password1",
    "user2": "password2"
}


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username  # Store username in session
            authenticated_users.add(username)
            return redirect(url_for('index_get'))
        else:
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error=error_message)
    return render_template('login.html')

# Custom decorator for login_required


def login_required(func):
    def wrapper(*args, **kwargs):
        if 'username' not in session or session['username'] not in authenticated_users:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__  # Preserve the original function name
    return wrapper


@app.route('/')
@login_required
def index_get():
    return render_template('base.html')


@app.route('/null/predict', methods=['POST'])
@login_required
def predict():
    logging.debug('Received request to /predict endpoint')
    text = request.get_json().get('message')
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)


def config():
    return None

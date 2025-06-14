from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

WORDS = ['python', 'flask', 'computer', 'keyboard', 'program']

MAX_ATTEMPTS = 6

def initialize_game():
    word = random.choice(WORDS)
    session['word'] = word
    session['display'] = ['_' for _ in word]
    session['guessed_letters'] = []
    session['attempts'] = MAX_ATTEMPTS
    session['game_over'] = False
    session['message'] = ''

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word' not in session:
        initialize_game()

    if request.method == 'POST':
        guess = request.form['guess'].lower()

        if session['game_over']:
            return redirect(url_for('index'))

        if guess in session['guessed_letters']:
            session['message'] = f"You already guessed '{guess}'!"
        else:
            session['guessed_letters'].append(guess)

            if guess in session['word']:
                for i, letter in enumerate(session['word']):
                    if letter == guess:
                        session['display'][i] = guess
                session['message'] = f"Good guess! '{guess}' is correct."
            else:
                session['attempts'] -= 1
                session['message'] = f"Wrong guess! '{guess}' is not in the word."

        if '_' not in session['display']:
            session['game_over'] = True
            session['message'] = f"🎉 You guessed the word '{session['word']}' correctly!"

        elif session['attempts'] <= 0:
            session['game_over'] = True
            session['message'] = f"💀 Game over! The word was '{session['word']}'"

    return render_template('index.html',
                           display=session['display'],
                           guessed=session['guessed_letters'],
                           attempts=session['attempts'],
                           message=session['message'],
                           game_over=session['game_over'])

@app.route('/restart')
def restart():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

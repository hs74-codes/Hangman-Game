from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session management


# Predefined word list
WORDS = ['apple', 'banana', 'grape', 'orange', 'melon']

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word' not in session:
        session['word'] = random.choice(WORDS)
        session['display'] = ['_' for _ in session['word']]
        session['guessed'] = []
        session['attempts'] = 6

    message = ""
    word = session['word']
    display_word = session['display']
    guessed_letters = session['guessed']
    attempts_left = session['attempts']

    if request.method == 'POST':
        guess = request.form['guess'].lower()

        if not guess.isalpha() or len(guess) != 1:
            message = "❌ Enter a single valid letter."
        elif guess in guessed_letters:
            message = "⚠️ You already guessed that letter."
        else:
            guessed_letters.append(guess)
            if guess in word:
                message = "✅ Correct!"
                for i, letter in enumerate(word):
                    if letter == guess:
                        display_word[i] = guess
            else:
                attempts_left -= 1
                message = f"❌ Incorrect! Attempts left: {attempts_left}"

        session['guessed'] = guessed_letters
        session['display'] = display_word
        session['attempts'] = attempts_left

        if '_' not in display_word:
            message = f"🎉 You won! The word was '{word}'."
        elif attempts_left == 0:
            message = f"💀 Game Over! The word was '{word}'."

    return render_template('index.html',
                           display_word=" ".join(session['display']),
                           guessed_letters=", ".join(session['guessed']),
                           attempts_left=session['attempts'],
                           message=message,
                           game_over=('_' not in session['display'] or session['attempts'] == 0))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

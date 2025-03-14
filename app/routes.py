from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game')
def game():
    mode = request.args.get('mode', 'competitive')  # Default to competitive if no mode
    return render_template('index.html', game_mode=mode)

if __name__ == '__main__':
    app.run(debug=True)
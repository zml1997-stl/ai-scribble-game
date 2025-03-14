from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/game')
def game():
    mode = request.args.get('mode', 'competitive')
    return render_template('index.html', game_mode=mode)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    drawing = data.get('drawing')  # Base64-encoded image
    description = data.get('description')

    if not drawing or not description:
        return jsonify({
            'success': False,
            'message': 'Please provide both a drawing and a description!'
        }), 400

    # For now, just echo back a success message
    # Later, we'll process with Gemini API and multiplayer logic
    response_message = f"Received your drawing and description: '{description}'"
    return jsonify({
        'success': True,
        'message': response_message
    })

if __name__ == '__main__':
    app.run(debug=True)
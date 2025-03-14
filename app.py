from flask import Flask, render_template, request, session, redirect, url_for
import requests
import os
import random
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')  # Set in Heroku config vars
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key')  # Set in Heroku config vars

# Mock data (replace with Gemini API later)
SAMPLE_PROMPTS = [
    "Help a penguin win a race against a cheetah.",
    "Stop a leaky dam with something unexpected.",
    "Prevent a volcano from erupting using only kitchen items."
]
SAMPLE_TWISTS = [
    "It’s now nighttime—adapt your solution!",
    "The weather turns rainy—how does that change things?",
    "A rival appears—make it competitive!"
]

# Game state storage (session-based for simplicity; replace with DB/WebSockets for true multiplayer)
def init_game_state():
    if 'game_state' not in session:
        session['game_state'] = {
            'prompt': None,
            'twist': None,
            'mode': 'competitive',  # Default mode
            'players': {},  # {player_id: {'description': ..., 'drawing': ..., 'scores': ..., 'votes': ...}}
            'round': 1,
            'max_rounds': 5,
            'phase': 'drawing',  # drawing, voting, results
            'start_time': None,
            'power_ups': {'jammer': 0, 'hint': 0, 'double': 0},
            'feedback': {},
            'leaderboard': {}
        }
    if 'player_id' not in session:
        session['player_id'] = f"player_{random.randint(1000, 9999)}"

def generate_prompt():
    try:
        response = requests.post(
            'https://api.gemini.ai/v1/generate',  # Hypothetical endpoint
            headers={'Authorization': f'Bearer {GEMINI_API_KEY}'},
            json={'prompt': 'Create a fun, quirky problem-solving scenario for a drawing game.', 'max_length': 50}
        )
        return response.json().get('text', random.choice(SAMPLE_PROMPTS))
    except Exception:
        return random.choice(SAMPLE_PROMPTS)

def generate_twist():
    try:
        response = requests.post(
            'https://api.gemini.ai/v1/generate',
            headers={'Authorization': f'Bearer {GEMINI_API_KEY}'},
            json={'prompt': 'Add a surprising twist to a problem-solving scenario.', 'max_length': 30}
        )
        return response.json().get('text', random.choice(SAMPLE_TWISTS))
    except Exception:
        return random.choice(SAMPLE_TWISTS)

def evaluate_description(prompt, description, twist=None):
    full_prompt = f"{prompt} {'Twist: ' + twist if twist else ''}"
    try:
        response = requests.post(
            'https://api.gemini.ai/v1/evaluate',
            headers={'Authorization': f'Bearer {GEMINI_API_KEY}'},
            json={'prompt': full_prompt, 'solution': description}
        )
        data = response.json()
        return (
            data.get('feedback', f"AI says: '{description}' is intriguing!"),
            {'effectiveness': data.get('effectiveness', random.randint(5, 10)),
             'creativity': data.get('creativity', random.randint(5, 10))}
        )
    except Exception:
        return (
            f"AI imagines: '{description}' could work with some luck!",
            {'effectiveness': random.randint(5, 10), 'creativity': random.randint(5, 10)}
        )

@app.route('/', methods=['GET', 'POST'])
def game():
    init_game_state()
    state = session['game_state']
    player_id = session['player_id']

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'start_game':
            state['prompt'] = generate_prompt()
            state['twist'] = None
            state['phase'] = 'drawing'
            state['start_time'] = datetime.utcnow().isoformat()
            state['players'] = {}
            state['feedback'] = {}

        elif action == 'submit_solution':
            description = request.form.get('description')
            drawing = request.form.get('drawing', 'placeholder')  # Canvas data (to be added later)
            state['players'][player_id] = {
                'description': description,
                'drawing': drawing,
                'scores': None,
                'votes': 0
            }
            if state['mode'] == 'collaborative' and len(state['players']) == 1:
                state['phase'] = 'drawing'  # Wait for more players
            else:
                state['phase'] = 'voting'

        elif action == 'vote':
            voted_player = request.form.get('vote_for')
            if voted_player and voted_player != player_id:
                state['players'][voted_player]['votes'] += 1

        elif action == 'use_power_up':
            power_up = request.form.get('power_up')
            if power_up in state['power_ups'] and state['power_ups'][power_up] > 0:
                state['power_ups'][power_up] -= 1
                if power_up == 'hint':
                    state['feedback'][player_id] = "Hint: Think outside the box!"
                elif power_up == 'double':
                    state['players'][player_id]['double'] = True
                elif power_up == 'jammer':
                    state['twist'] = None  # Simplistic jammer effect

        elif action == 'next_round':
            for p_id, data in state['players'].items():
                if not data.get('scores'):
                    feedback, scores = evaluate_description(state['prompt'], data['description'], state['twist'])
                    state['players'][p_id]['scores'] = scores
                    state['feedback'][p_id] = feedback
                    total_score = scores['effectiveness'] + scores['creativity'] + data['votes']
                    state['leaderboard'][p_id] = state['leaderboard'].get(p_id, 0) + total_score
            state['round'] += 1
            if state['round'] > state['max_rounds']:
                state['phase'] = 'results'
            else:
                state['prompt'] = generate_prompt()
                state['twist'] = random.random() < 0.3 and generate_twist() or None
                state['phase'] = 'drawing'
                state['players'] = {}

        elif action == 'set_mode':
            state['mode'] = request.form.get('mode', 'competitive')
            state['round'] = 1
            state['leaderboard'] = {}
            return redirect(url_for('game'))

    # Timer check for phase transition (simplified)
    if state['start_time']:
        elapsed = datetime.utcnow() - datetime.fromisoformat(state['start_time'])
        if state['phase'] == 'drawing' and elapsed > timedelta(minutes=2):
            state['phase'] = 'voting'
        elif state['phase'] == 'voting' and elapsed > timedelta(minutes=4):
            state['phase'] = 'results'

    session['game_state'] = state
    return render_template('game.html', state=state, player_id=player_id)

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('game_state', None)
    session.pop('player_id', None)
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

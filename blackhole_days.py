import math
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

# XP Table (level: total xp)
xp_table = {
    0: 0,
    1: 462,
    2: 2688,
    3: 5885,
    4: 11777,
    5: 29217,
    6: 46289,
    7: 63592,
    8: 74373,
    9: 85516,
    10: 95033,
    11: 105630,
    12: 124446,
    13: 145782,
    14: 169932,
    15: 197316,
    16: 228354,
    17: 263508,
    18: 303366,
    19: 348516,
    20: 399672,
    21: 457632,
    # Extrapolated values for levels 22-25 (these are predictions based on pattern analysis)
    22: 522776,  # Extrapolated - not official
    23: 596388,  # Extrapolated - not official
    24: 679652,  # Extrapolated - not official
    25: 773932,  # Extrapolated - not official
}

def level_to_xp(level):
    level_base = int(level)
    progress = level - level_base  # decimal part of level

    if level_base in xp_table and (level_base + 1) in xp_table:
        current_total_xp = xp_table[level_base]
        next_level_xp = xp_table[level_base + 1]
        xp_to_next_level = next_level_xp - current_total_xp

        interpolated_xp = current_total_xp + (progress * xp_to_next_level)
        return interpolated_xp
    else:
        return None  # Handle cases outside the table

def xp_to_level(xp):
    for level in sorted(xp_table.keys()):
        if xp < xp_table[level]:
            prev_level = level - 1
            if prev_level < 0:
                return 0  # Handle case where XP is below level 0
            prev_total_xp = xp_table[prev_level]
            xp_to_next = xp_table[level] - prev_total_xp
            progress = (xp - prev_total_xp) / xp_to_next if xp_to_next > 0 else 0
            return prev_level + progress
    return max(xp_table.keys())  # If over max level, return highest

# Data storage functions
def get_data_path():
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    # Create data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    return data_dir

def save_user(user_data):
    data_dir = get_data_path()
    user_file = os.path.join(data_dir, f"{user_data['username']}.json")
    
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=4)
    
    return True

def load_user(username):
    data_dir = get_data_path()
    user_file = os.path.join(data_dir, f"{username}.json")
    
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    
    return None

def get_all_users():
    data_dir = get_data_path()
    users = []
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.json'):
                username = file[:-5]  # Remove .json extension
                users.append(username)
    
    return users

def save_project(username, project_data):
    user_data = load_user(username)
    
    if user_data is None:
        return False
    
    if 'projects' not in user_data:
        user_data['projects'] = {}
    
    user_data['projects'][project_data['name']] = {
        'xp': project_data['xp'],
        'description': project_data.get('description', ''),
        'date_added': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return save_user(user_data)

def save_simulation(username, simulation_data):
    user_data = load_user(username)
    
    if user_data is None:
        return False
    
    if 'simulations' not in user_data:
        user_data['simulations'] = {}
    
    simulation_id = datetime.now().strftime('%Y%m%d%H%M%S')
    
    user_data['simulations'][simulation_data['name']] = {
        'id': simulation_id,
        'starting_level': simulation_data['starting_level'],
        'current_xp': simulation_data['current_xp'],
        'projects': simulation_data['projects'],
        'target_level': simulation_data.get('target_level', 25),
        'date_saved': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return save_user(user_data)

# ASCII art for the web page
ascii_art = r"""
 ____  _               _____ _  ___    _  ____  _      ______   _____      __     _______ 
 |  _ \| |        /\   / ____| |/ / |  | |/ __ \| |    |  ____| |  __ \   /\\ \   / / ____|
 | |_) | |       /  \ | |    | ' /| |__| | |  | | |    | |__    | |  | | /  \\ \_/ / (___  
 |  _ <| |      / /\ \| |    |  < |  __  | |  | | |    |  __|   | |  | |/ /\ \\   / \___ \ 
 | |_) | |____ / ____ \ |____| . \| |  | | |__| | |____| |____  | |__| / ____ \| |  ____) |
 |____/|______/_/    \_\_____|_|\_\_|  |_|\____/|______|______| |_____/_/    \_\_| |_____/
              CODEX 42 XP CALCULATOR
"""

# Create Flask application
app = Flask(__name__)
app.secret_key = 'codex42_secret_key'  # For session management

@app.route('/')
def home():
    users = get_all_users()
    return render_template('index.html', ascii_art=ascii_art, users=users)

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    current_level = data.get('current_level')
    
    if not username or not current_level:
        return jsonify({'success': False, 'message': 'Missing required data'}), 400
    
    try:
        current_level = float(current_level)
        current_xp = level_to_xp(current_level)
        
        if current_xp is None:
            return jsonify({'success': False, 'message': 'Invalid level input'}), 400
            
        user_data = {
            'username': username,
            'current_level': current_level,
            'current_xp': current_xp,
            'projects': {}
        }
        
        save_user(user_data)
        return jsonify({'success': True, 'message': 'User created successfully'})
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid level format'}), 400

@app.route('/load_user/<username>')
def get_user(username):
    user_data = load_user(username)
    
    if user_data:
        return jsonify({'success': True, 'user': user_data})
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404

@app.route('/save_project', methods=['POST'])
def add_project():
    data = request.json
    username = data.get('username')
    project_name = data.get('project_name')
    project_xp = data.get('project_xp')
    project_desc = data.get('project_description', '')
    
    if not username or not project_name or project_xp is None:
        return jsonify({'success': False, 'message': 'Missing required data'}), 400
    
    try:
        project_xp = float(project_xp)
        project_data = {
            'name': project_name,
            'xp': project_xp,
            'description': project_desc
        }
        
        success = save_project(username, project_data)
        
        if success:
            return jsonify({'success': True, 'message': 'Project saved successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to save project'}), 500
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid XP format'}), 400

@app.route('/save_simulation', methods=['POST'])
def save_sim():
    data = request.json
    username = data.get('username')
    simulation_name = data.get('name')
    simulation_data = data.get('simulation_data')
    
    if not username or not simulation_name or not simulation_data:
        return jsonify({'success': False, 'message': 'Missing required data'}), 400
    
    simulation = {
        'name': simulation_name,
        'starting_level': simulation_data.get('startingLevel'),
        'current_xp': simulation_data.get('currentXP'),
        'projects': simulation_data.get('projects', []),
        'target_level': simulation_data.get('targetLevel', 25)
    }
    
    success = save_simulation(username, simulation)
    
    if success:
        return jsonify({'success': True, 'message': 'Simulation saved successfully'})
    else:
        return jsonify({'success': False, 'message': 'Failed to save simulation'}), 500

@app.route('/get_simulations/<username>', methods=['GET'])
def get_simulations(username):
    user_data = load_user(username)
    
    if not user_data or 'simulations' not in user_data:
        return jsonify({'success': True, 'simulations': {}})
    
    return jsonify({'success': True, 'simulations': user_data['simulations']})

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    current_level = data.get('current_level')
    project_xp = data.get('project_xp')
    
    try:
        current_level = float(current_level)
        project_xp = float(project_xp)
        
        current_xp = level_to_xp(current_level)
        
        if current_xp is None:
            # For high levels outside the table, try to approximate the XP
            if current_level > max(xp_table.keys()):
                # Use the last known level and extrapolate
                max_level = max(xp_table.keys())
                max_xp = xp_table[max_level]
                # Simple extrapolation: assume similar growth rate
                estimated_xp = max_xp * (1.15 ** (current_level - max_level))
                current_xp = estimated_xp
            else:
                return jsonify({'success': False, 'message': 'Invalid level input'}), 400
            
        new_xp = current_xp + project_xp
        new_level = xp_to_level(new_xp)
        
        return jsonify({
            'success': True, 
            'current_xp': current_xp, 
            'new_xp': new_xp, 
            'new_level': new_level
        })
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid input format'}), 400

def create_templates_folder():
    # Create templates folder if it doesn't exist
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')
    
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    return templates_dir

if __name__ == "__main__":
    create_templates_folder()
    app.run(debug=True)

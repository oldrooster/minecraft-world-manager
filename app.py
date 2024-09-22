from flask import Flask, jsonify, request, render_template, send_from_directory
import os
from jinja2 import Environment, FileSystemLoader
# import shutil
import docker

app = Flask(__name__, static_url_path='', static_folder='static')

# Get the Minecraft container name from an environment variable, or default to "minecraft"
minecraft_container_name = os.getenv('MINECRAFT_CONTAINER', 'minecraft')

# Initialize Docker client
client = docker.from_env()

# Directory paths
TEMPLATES_DIR = 'templates'
WORLD_PROPERTIES_DIR = '/configs'
MINECRAFT_ROOT_DIR = '/minecraft'

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/worlds', methods=['GET'])
def list_worlds():
    worlds = [f[:-len('.properties')] for f in os.listdir(WORLD_PROPERTIES_DIR) if f.endswith('.properties')]
    return jsonify(worlds)

@app.route('/world_properties/<world>', methods=['GET'])
def get_world_properties(world):
    properties_file = os.path.join(WORLD_PROPERTIES_DIR, f"{world}.properties")
    
    if not os.path.exists(properties_file):
        return jsonify({"error": "World not found"}), 404
    
    with open(properties_file) as f:
        properties = f.readlines()
    
    props_dict = {}
    for line in properties:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            props_dict[key] = value
    
    return jsonify(props_dict)

@app.route('/create', methods=['POST'])
def create_minecraft():
    data = request.json
    world_name = data.get('world')
    level_seed = data.get('level_seed', '')
    game_mode = data.get('game_mode', 'survival')
    difficulty = data.get('difficulty', 'normal')
    default_player_permission_level = data.get('default_player_permission_level', 'member')
    level_type = data.get('level_type', 'minecraft\:normal')
    allow_cheats = 'true' if data.get('allow_cheats', False) else 'false'
    
    if not world_name:
        return jsonify({"error": "No world name specified"}), 400
    
    # Load the Jinja2 template
    template = env.get_template('server.properties.j2')
    properties_content = template.render(
        level_name=world_name,
        level_seed=level_seed,
        game_mode=game_mode,
        difficulty=difficulty,
        allow_cheats=allow_cheats,
        level_type=level_type,
        default_player_permission_level = default_player_permission_level
    )
    
    properties_file_path = os.path.join(WORLD_PROPERTIES_DIR, f"{world_name}.properties")
    minecraft_world_properties_path = os.path.join(MINECRAFT_ROOT_DIR, f"server.properties")
    # Write the new server.properties file
    with open(properties_file_path, 'w') as file:
        file.write(properties_content)

    with open(minecraft_world_properties_path, 'w') as file:
        file.write(properties_content)


    # Restart the Minecraft Docker container
    try:
        container = client.containers.get(minecraft_container_name)
        container.restart()  # Restart the container
        return jsonify({'status': f'Successfully created {world_name} and restarted Minecraft container: {minecraft_container_name}'})
    except docker.errors.NotFound:
        return jsonify({'error': 'Minecraft container not found: {minecraft_container_name}'}), 404
    except docker.errors.APIError as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

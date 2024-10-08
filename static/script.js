async function loadWorlds() {
    let response = await fetch('/worlds');
    let worlds = await response.json();
    let dropdown = document.getElementById('worlds-dropdown');
    dropdown.innerHTML = '<option value="" disabled selected> - Select - </option>'; // Add placeholder option
    worlds.forEach(world => {
        let option = document.createElement('option');
        option.value = world;
        option.textContent = world;
        dropdown.appendChild(option);
    });
}

async function createServer() {
    let worldName = document.getElementById('new-world-name').value;
    let levelSeed = document.getElementById('level-seed').value;
    let gameMode = document.getElementById('game-mode').value;
    let difficulty = document.getElementById('difficulty').value;
    let allowCheats = document.getElementById('allow-cheats').checked;
    let defaultPlayerPermissionLevel = document.getElementById('default-player-permission-level').value;
    let levelType = document.getElementById('level-type').value;

    if (!worldName) {
        document.getElementById('status').textContent = 'Please enter a world name.';
        return;
    }

    let response = await fetch('/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            world: worldName,
            level_seed: levelSeed,
            game_mode: gameMode,
            difficulty: difficulty,
            allow_cheats: allowCheats,
            default_player_permission_level: defaultPlayerPermissionLevel,
            level_type: levelType
        })
    });
    let status = await response.json();
    document.getElementById('status').textContent = status.status || status.error;
    
    if (status.status) {
        // Reload the worlds dropdown to include the new world
        await loadWorlds();
    }
}

async function loadWorldProperties() {
    let world = document.getElementById('worlds-dropdown').value;
    if (!world) return;

    let response = await fetch(`/world_properties/${world}`);
    if (response.ok) {
        let properties = await response.json();
        document.getElementById('new-world-name').value = world;
        document.getElementById('level-seed').value = properties['level-seed'] || '';
        document.getElementById('game-mode').value = properties['gamemode'] || 'survival';
        document.getElementById('difficulty').value = properties['difficulty'] || 'normal';
        document.getElementById('allow-cheats').checked = (properties['allow-cheats'] === 'true');
        document.getElementById('default-player-permission-level').value = properties['default-player-permission-level'] || 'operator';
        document.getElementById('level-type').value = properties['level-type'] || 'minecraft\:normal';
    } else {
        document.getElementById('status').textContent = 'Failed to load world properties.';
    }
}

document.getElementById('worlds-dropdown').addEventListener('change', loadWorldProperties);

// Load available worlds on page load
window.onload = loadWorlds;

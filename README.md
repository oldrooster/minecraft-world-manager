# Simple Minecraft World Manager

Simple Minecraft World Manager is a web-based application that allows you to easily manage and switch between Minecraft Bedrock Edition worlds. It provides the ability to create new worlds with customizable settings, manage multiple world configurations, and restart the Minecraft server as needed. All server properties are configurable via a simple web interface.

## Features

- **Create New Worlds**: Create a new world by specifying important Minecraft server properties like world name, level seed, game mode, difficulty, and more.
- **Manage Existing Worlds**: Switch between previously created worlds via a dropdown list, and load the specific server settings for each.
- **Server Properties Management**: Customize the Minecraft `server.properties` file with options like level name, game mode, difficulty, max players, and other settings.
- **Persistent Storage**: Each world's `server.properties` file is saved in a dedicated directory (`/configs`), making it easy to manage and switch between worlds.
- **Docker Integration**: The app can restart the Minecraft Docker container whenever a new world is selected or created.

## Prerequisites

- **Docker** and **Docker Compose** installed on your system
- A running Minecraft Bedrock server container.
- Python 3.8+ with the following libraries:
  - Flask
  - Jinja2
  - Docker SDK for Python

## Getting Started

### Clone the repository

```bash
git clone https://github.com/oldrooster/minecraft-world-manager.git
cd minecraft-world-manager

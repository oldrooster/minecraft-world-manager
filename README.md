# Simple Minecraft World Manager

Simple Minecraft World Manager is a web-based application that allows you to easily manage and switch between Minecraft Bedrock Edition worlds. It provides the ability to create new worlds with customizable settings, manage multiple world configurations, and restart the Minecraft server as needed. All server properties are configurable via a simple web interface.

## Why did I create this?

I have kids who like to play minecraft. With a single bedrock container at home, I was getting tired of needing to reconfigure it for new worlds they could play on. While other feature which server managers existed. They were far too complicated and overkill for my requirements with young kids. I simply wanted a web based tool to manage a single instance and switch between worlds/create new worlds in a self service manner. Very simple, no auth so probably horribly insecure, but thats fine for my use case :) The kids can manage it easily, and peace reins again.

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

## Docker

### Example Compose File
```
services:
 minecraft-world-manager:
   image: oldrooster/minecraft-world-manager:latest
   ports:
     - "5000:5000"
   environment:
     - MINECRAFT_CONTAINER=minecraft       
   volumes:
     - /var/run/docker.sock:/var/run/docker.sock
     - /path/to/minecraft/root:/minecraft
     - /path/to/minecraft-world-manager/configs:/configs
```

### Volume Mounts
* `/var/run/docker.sock:/var/run/docker.sock` - Allows the service to restart the minecraft docker container when worlds are changed.
* `/path/to/minecraft/root:/minecraft` - Path to root of minecraft container, where you can find `server.properties`
* `/path/to/minecraft-world-manager/configs:/configs` - Path to store minecraft config files for each world.

### Clone the repository

```bash
git clone https://github.com/oldrooster/minecraft-world-manager.git
cd minecraft-world-manager

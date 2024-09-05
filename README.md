# Backend for Magic_Collection_Game API

This is a backend service for a magic_collection_game application, implemented using Flask. It provides endpoints to manage game data and perform actions like starting a new game and flying to a new location.

## Features

Start a New Game: Create a new game with a player and initial location.<br>
Fly to a New Location: Move to a new location within the game, consuming resources and updating the game state.

## Installation

> Clone the Repository

    `git clone https://github.com/Yoohoo-cf/owl_game_backend.git`
    `cd owl_game_backend`

## Install Dependencies

`pip install -r requirements.txt`

> Ensure you have the following packages in your requirements.txt:

    * Flask
    * Flask-Cors
    * mysql-connector-python
    * python-dotenv

## Configuration

**Create a .env File**

- The .env file should be located in the root directory of the project and include the following environment variables:

  HOST=<your-database-host><br>
  PORT=<your-database-port><br>
  DB_NAME=<your-database-name><br>
  DB_USER=<your-database-user><br>
  DB_PASS=<your-database-password><br>

**Database Configuration**

- Ensure that your MySQL database is accessible from the environment where the Flask application is running and that it has the correct credentials and settings.

## Endpoints

/flyto

    Method: GET
    Description: Moves the game to a new location and consumes resources.
    Query Parameters:
        game: The ID of the game.
        dest: The destination location code.
        consumption: Energy consumption.
    Example Request:

    http://127.0.0.1:7000/flyto?game=VAFyWkaMC4H1jWxR44Tl&dest=ESCF&consumption=246

    Response: JSON data representing the updated game state.

/newgame

    Method: GET
    Description: Starts a new game with a specified player and location.
    Query Parameters:
        player: The name of the player.
        loc: The initial location code.
    Example Request:

    http://127.0.0.1:7000/newgame?player=Remy&loc=LFDZ

    Response: JSON data representing the initial game state.

## Running the Application

To run the Flask application, use the following command:

`python3 app.py` on MacOS or `python app.py` on Windows

The application will be accessible at http://127.0.0.1:7000 by default. If you need to change the port or host, adjust the environment variables or command line arguments accordingly.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

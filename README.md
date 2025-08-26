# Mastermind game

## Features
- Starts game with a random 4 digit number via Random API
- Submit guess and receive feedback(hints)
- Track game history and timing per attempts
- Health check which tracks all the current and past games

## Game Rules

- Secret code consists of 4 digits (0-7)
- Players have 10 attempts to guess correctly
- Feedback provided for each guess:
  - **Correct digits**: Numbers that appear in the secret code
  - **Correct locations**: Numbers in the right position
- Game ends when code is guessed correctly or 10 attempts are used

## API endpoints
### Game Management
- `POST /mastermind/start-game` - Start a new game
- `POST /mastermind/end-game` - End an active game
- `GET /mastermind/health` - System health check

### Gameplay
- `POST /mastermind/make-guess` - Submit a 4-digit guess
- `GET /mastermind/get-status?game_id={id}` - Get current game status

### History & Analytics
- `GET /mastermind/get-history?game_id={id}` - Get specific game history
- `GET /mastermind/get-games` - Get all games history

## How to run 

```bash
# create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# cd into app to run FASTAPI
cd app

# Start the development server
uvicorn app.main:app --reload

# Server will be available at:
# http://localhost:8000
# API documentation at: http://localhost:8000/docs (makes it easier to run and test)
```

### Terminal/curl Commands (Easier testing done on the /docs website)

```bash
# Start a new game
curl -X POST "http://localhost:8000/mastermind/start-game"
# Response: {"game_id": 1234}

# Make a guess
curl -X POST "http://localhost:8000/mastermind/make-guess" \
  -H "Content-Type: application/json" \
  -d '{"guess": "1234", "game_id": 1234}'

# Check game status
curl -X GET "http://localhost:8000/mastermind/get-status?game_id=1234"

# Get game history
curl -X GET "http://localhost:8000/mastermind/get-history?game_id=1234"

# System health check
curl -X GET "http://localhost:8000/mastermind/health"

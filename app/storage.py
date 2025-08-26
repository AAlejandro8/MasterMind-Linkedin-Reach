from collections import defaultdict
import random
import requests
from game import check_attempt
import time
import datetime
from fastapi import HTTPException

# local storage which deletes after the program is ended
games = defaultdict(dict)

def create_game() -> int:
      url = 'https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new'
      number = []
      # Call the api
      try:
            response = requests.get(url)
            if response.status_code == 200:
                  response_text = response.text
                  number = [int(x) for x in response_text.split()]
            else:
                  print(response.status_code)
                  print(response.text)

      except requests.exceptions.RequestException as e:
            print(f"Error occured: {e}")

      # make a game id could be implemented better using UUID
      game_id = random.randint(1000,9999)
      # template per game instance
      games[game_id] = {
            "secret_number": number,
            "attempts": [],
            "status": 'ongoing',
            "attempt_count": 0,
            "start_time": time.time(),
            "last_attempt_time": None,
            "end_time": None
      }

      return game_id

# end the timer at the end of the game
def end_timer(game_id: int):
      if game_id not in games:
            raise HTTPException(status_code=404, detail="Game not found")
      
      start_time = games[game_id]['start_time']
      if start_time is None:
            raise HTTPException(status_code=400, detail="Error: Timer wasnt started")
      
      end_time = time.time()

      return end_time

# formating for the raw time stamps
def format_timestamp(ts):
    return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Helper method to log the guess made
def log_entry(game_id, guess, correct_loc, correct_num, time_per_attempt, status = None):
      games[game_id]['attempts'].append({
            "guess": ''.join(str(x) for x in guess),
            "feedback": {"correct digits:": correct_num, "correct_locations: ": correct_loc},
            "time_per_attempt": round(time_per_attempt, 2)
      })

      games[game_id]['attempt_count'] += 1

      if status is not None:
            games[game_id]['status'] = status
      

# add the guess to the the attempt 
def add_guess(guess: list, game_id: int):
      if game_id not in games:
            raise HTTPException(status_code=404, detail="Game not found")
      
      # get the game to work on it
      game = games[game_id]

      if game['status'] != 'ongoing':
            raise HTTPException(status_code=400, detail=f"Game status is {game['status']}, cannot make more guesses.")
      if game['attempt_count'] > 10:
            raise HTTPException(status_code=400, detail="Game attempts past 10, cannot guess.")
      
      # calculate the time since the last attempt
      now = time.time()
      # first attempt case
      if game["last_attempt_time"] is None:
            time_since_last = now - game["start_time"]
      else:
            time_since_last = now - game["last_attempt_time"]

      # update time
      game["last_attempt_time"] = now

      # check the guess against the secret number
      correct_num, correct_loc = check_attempt(guess, game["secret_number"])

      # user guessed correct!
      if correct_num == 4 and correct_loc == 4:
            log_entry(game_id, guess, correct_loc, correct_num, time_since_last, status='Won')
            return f"player guesses '{' '.join(str(x) for x in guess)}: All correct!'"
      
      # used all their hints so lost
      elif game['attempt_count'] + 1 == 10:
            log_entry(game_id, guess, correct_loc, correct_num, time_since_last,status='lost')
            return f"player used all their hints - game over!"
      
      # user didnt get one correct
      elif correct_num == 0 and correct_loc == 0:
            log_entry(game_id, guess, correct_loc, correct_num, time_since_last)
            return f"player guesses '{' '.join(str(x) for x in guess)}: all Incorrect!'"    
        
      # return the hints; some numbers correct
      else:
            num_str = 'number' if correct_num == 1 else 'numbers'
            loc_str = 'location' if correct_loc == 1 else 'locations'
            log_entry(game_id, guess, correct_loc, correct_num, time_since_last)
            return f"Player guesses '{' '.join(str(x) for x in guess)}', game responds: {correct_num} correct {num_str} and {correct_loc} correct {loc_str}"
            
# return history on one game
def get_history(game_id: int):
      if game_id not in games:
            raise HTTPException(status_code=404, detail="Game not found!")
      
      # copy the game to prevent overriding
      game = games[game_id].copy()
      
      # format secret number based on status to prevent cheating.
      if game["status"] == "ongoing":
            game["secret_number"] = "****"
      else: 
            game["secret_number"] = ''.join(str(x) for x in game["secret_number"])
      
      # raw timestamp formating
      if game.get('end_time'):
            game['end_time'] = format_timestamp(game['end_time'])
      if game.get('start_time'):
            game['start_time'] = format_timestamp(game['start_time'])
      if game.get('last_attempt_time'):
            game['last_attempt_time'] = format_timestamp(game['last_attempt_time'])
      return game


def get_all_game_history():
      # format the games better for readability 
      formatted_games = {}
      # game id, game history 
      for gid, game in games.items():
        game_copy = game.copy()

        # format secret number based on status to prevent cheating.
        if game_copy["status"] == "ongoing":
            game_copy["secret_number"] = "****"
        else:
            game_copy["secret_number"] = ''.join(str(x) for x in game_copy["secret_number"])

        # formatted time stamps
        if game_copy.get('end_time'):
            game_copy['end_time'] = format_timestamp(game_copy['end_time'])
        if game_copy.get('start_time'):
            game_copy['start_time'] = format_timestamp(game_copy['start_time'])
        if game_copy.get('last_attempt_time'):
            game_copy['last_attempt_time'] = format_timestamp(game_copy['last_attempt_time'])
    
        formatted_games[gid] = game_copy
      return formatted_games


def get_status(game_id: int):
      if game_id not in games:
            raise HTTPException(status_code=404, detail="Game not found!")
      
      return games[game_id]['status']

def end_game(game_id: int):
      if game_id not in games:
            raise HTTPException(status_code=404, detail="Game not found!")
      if games[game_id]['status'] != 'ongoing':
            raise HTTPException(status_code=400, detail="Game is already complete!")
      
      games[game_id]['status'] = 'quit'
      games[game_id]['end_time'] = end_timer(game_id)
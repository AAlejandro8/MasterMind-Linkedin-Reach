from fastapi import APIRouter
import schemas 
from game import user_input
from storage import create_game, add_guess, get_history, get_status, end_game, get_all_game_history

router = APIRouter()

@router.post('/make-guess',
              response_model=schemas.PlayerGuessResponse,
              summary="submit a guess",
              description="user makes a guess with 4 digits (0-7) and recives feedback.")
def make_guess(player_guess: schemas.PlayerGuess):
      """Submit a 4-digit guess and recieve feedback on that guess"""
      result = add_guess(user_input(player_guess.guess), (player_guess.game_id))
      return (schemas.PlayerGuessResponse(message=result if result is not None else ""))

@router.post('/start-game', 
             response_model=schemas.GameStartReturn,
             summary="start new game",
             description="creates a new game (mastermind) is created with a 4-digit secret code provided by an API")
def start_game():
      """ Start the game with an API generated 4-digit secret code"""
      game_id = create_game()
      return schemas.GameStartReturn(game_id=game_id)

@router.post('/end-game',
             summary="end the game by id",
             description="user chooses to end the game")
def end_game_by_id(game_id: schemas.PlayerEndGame):
      end_game(game_id.game_id)
      return {"message": "Game Successfully ended"}

@router.get('/health',
            summary="check all active games",
            description="make a health check which returns all the active games")
def health_check():
      """health check of all the ongoing games"""
      all_games = get_all_game_history()
      return{
            "status": "healthy",
            "active_games": len([g for g in all_games.values() if g['status'] == 'ongoing']),
            "total_games": len(all_games)
      }

@router.get('/get-games',
            summary="get all the games",
            description="returns all games which are ended or ongoing")
def get_all_games():
      return get_all_game_history()

@router.get('/get-status',
             response_model=schemas.PlayerStatusResponse,
             summary="get status of a game",
             description="returns the status of a game based on the id")
def get_status_by_id(game_id: schemas.PlayerGetStatus):
      status_of_game = get_status(game_id.game_id)
      return schemas.PlayerStatusResponse(status=status_of_game)

@router.get('/history-by-id',
            summary="get the history of a game",
            description="able to get the history of a game which is helpful for hints")
def history_by_id(game_id: schemas.GameHistoryById):
      return get_history(game_id.game_id)



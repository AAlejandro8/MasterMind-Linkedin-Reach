from pydantic import BaseModel, Field
# player schemas
class PlayerGuess(BaseModel):
      guess: str
      game_id: int

class PlayerGuessResponse(BaseModel):
      message: str
      class Config:
        from_attributes = True

class PlayerEndGame(BaseModel):
     game_id: int

class PlayerGetStatus(BaseModel):
     game_id: int

class PlayerStatusResponse(BaseModel):
     status: str
     class Config:
          from_attributes = True

# game schemas
class GameHistoryById(BaseModel):
     game_id: int


class GameStartReturn(BaseModel):
     id: int = Field(..., alias="game_id")
     class Config:
        from_attributes = True
        populate_by_name = True
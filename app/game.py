# GAME LOGIC
from fastapi import HTTPException

#  normalize the input number
#  no negative and must be within range 0 - 7
def user_input(nums: str):
      if nums.startswith('-'):
            raise HTTPException(status_code=400, detail="No negative numbers allowed")
      if len(nums) != 4:
            raise HTTPException(status_code=400, detail="No numbers greater than 4 digits")
      
      guess = []
      for ch in nums:
            if not ch.isdigit():
                  raise HTTPException(status_code=400, detail="only digits allowed")
            if int(ch) > 7:
                  raise HTTPException(status_code=400, detail="no numbers greater than 7")
            guess.append(int(ch))

      return guess

# check the attempt algorithm
def check_attempt(player: list[int],computer: list[int]) -> tuple[int, int]:
      correct_number = 0
      correct_location = 0
      # make copies to prevent overriding original numbers
      computer_copy = computer.copy()
      player_copy = player.copy()

      # CASE: correct location; correct number
      for i in range(len(player)):
            # match number so it cant be matched for the second loop 
            if player[i] == computer[i]:
                  correct_location += 1
                  computer_copy[i] = player_copy[i] = -1

      # CASE: wrong location but right number
      # very important! prevents double counting in the case of duplicates
      for i in range(len(player)):
            # number isnt already matched and in the computer number
            if player_copy[i] != -1 and player_copy[i] in computer_copy:
                  correct_number += 1
                  # get the index of the number in the computer array
                  # eg: player = [1,3,5,6], computer = [1,2,3,4]
                  # computer_copy[computer_copy.index(3)]
                  # computer_copy[2] = -1
                  computer_copy[computer_copy.index(player_copy[i])] = -1

      
      return correct_number + correct_location, correct_location


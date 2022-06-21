from model.game_model import GameModel
from brownie import accounts, Game, chain
from bots.aggro_bot import Aggro

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

statsAllowance = 20
maxPlayers = 4
gameCost = '5 wei'

def test_model():
  empty_model = GameModel()
  empty_model.step()
  # one of the agents should have done something after 1 step
  assert (empty_model.game.ownerToPlayer(accounts[0])[player_struct.index("playerState")] != READY or
          empty_model.game.ownerToPlayer(accounts[1])[player_struct.index("playerState")] != READY or
          empty_model.game.ownerToPlayer(accounts[2])[player_struct.index("playerState")] != READY or
          empty_model.game.ownerToPlayer(accounts[3])[player_struct.index("playerState")] != READY)

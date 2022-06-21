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

  aa = empty_model.game.ownerToPlayer(accounts[0])
  ca = empty_model.game.ownerToPlayer(accounts[1])
  ra1 = empty_model.game.ownerToPlayer(accounts[2])
  ra2 = empty_model.game.ownerToPlayer(accounts[3])

  empty_model.step()

  # one of the agents should have done something after 1 step
  assert (aa[player_struct.index("playerState")] != READY or
          ca[player_struct.index("playerState")] != READY or
          ra1[player_struct.index("playerState")] != READY or
          ra2[player_struct.index("playerState")] != READY)

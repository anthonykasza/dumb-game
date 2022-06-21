from brownie import accounts, Game, chain
from bots.cautious_bot import Cautious

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

statsAllowance = 20
maxPlayers = 4
gameCost = '5 wei'

def test_bot():
  game = Game.deploy(statsAllowance, maxPlayers, gameCost, {'from': accounts[0]})

  game.registerPlayer(1, 1, 1, 13, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 12, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})

  bot = Cautious(game_addr=game.address, my_account=accounts[0])
  bot.register()
  bot.orient()
  bot.brace()
  chain.mine(1)

  assert (game.ownerToPlayer(bot.my_account)[player_struct.index("playerState")] == BRACED)

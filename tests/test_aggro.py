from brownie import accounts, Game, chain
from bots.aggro_bot import Aggro

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

def test_bot():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})

  game.registerPlayer(1, 1, 1, 13, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 12, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})

  bot = Aggro(game.address, accounts[0])
  bot.register()
  bot.orient()
  bot.select_target()
  bot.hit()

  assert (game.ownerToPlayer(accounts[1])[player_struct.index("hp")] == 0 and
          game.ownerToPlayer(bot.my_account)[player_struct.index("playerState")] == LUNGED)

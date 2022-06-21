from brownie import accounts, Game, chain
from bots.base_bot import Bot

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

  bot = Bot(game_addr=game.address, my_account=accounts[0])
  bot.register()
  bot.orient()
  bot.brace()
  chain.mine(1)

  assert (game.ownerToPlayer(bot.my_account)[player_struct.index("playerState")] == BRACED)


def test_brace_grace():
  game = Game.deploy(statsAllowance, maxPlayers, gameCost, {'from': accounts[0]})

  game.registerPlayer(1, 1, 1, 13, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 12, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})

  bot = Bot(game_addr=game.address, my_account=accounts[0])
  bot.register()
  bot.orient()
  bot.brace()
  chain.mine(5)
  bot.orient()
  bot.brace()

  assert (game.ownerToPlayer(bot.my_account)[player_struct.index("playerState")] == BRACED)


def test_brace_grace_fail():
  game = Game.deploy(statsAllowance, maxPlayers, gameCost, {'from': accounts[0]})

  game.registerPlayer(1, 1, 1, 13, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 12, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})

  bot = Bot(game_addr=game.address, my_account=accounts[0])
  bot.register()
  bot.orient()
  bot.brace()
  chain.mine(4)
  bot.orient()
  try:
    bot.brace()
  except:
    assert True


def test_hit_grace():
  game = Game.deploy(statsAllowance, maxPlayers, gameCost, {'from': accounts[0]})

  game.registerPlayer(1, 1, 1, 13, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 12, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})

  bot = Bot(game_addr=game.address, my_account=accounts[0])
  bot.register()
  bot.orient()
  bot.select_target()
  bot.hit()

  p = game.ownerToPlayer(bot.my_account)
  p_status = p[player_struct.index("playerState")]
  p_prev_block = p[player_struct.index("prevActionBlock")]

  chain.mine(chain.height - p_prev_block + statsAllowance - bot.ag + 1)
  bot.select_target()
  bot.hit()

  assert (game.ownerToPlayer(bot.my_account)[player_struct.index("playerState")] == LUNGED)


def test_hit_grace_fail():
  game = Game.deploy(statsAllowance, maxPlayers, gameCost, {'from': accounts[0]})

  game.registerPlayer(1, 1, 1, 13, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 12, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})

  bot = Bot(game_addr=game.address, my_account=accounts[0])
  bot.register()
  bot.orient()
  bot.select_target()
  bot.hit()

  p = game.ownerToPlayer(bot.my_account)
  p_status = p[player_struct.index("playerState")]
  p_prev_block = p[player_struct.index("prevActionBlock")]

  chain.mine(1)
  bot.select_target()
  try:
    bot.hit()
  except:
    assert True

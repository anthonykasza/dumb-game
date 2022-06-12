
from brownie import accounts, Game, chain

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2


def test_READY():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  chain.mine(1)
  assert game.ownerToPlayer(accounts[0])[player_struct.index("playerState")] == READY

def test_LUNGED():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  chain.mine(1)
  game.hit(accounts[0], {'from':accounts[1]})
  chain.mine(1)
  assert game.ownerToPlayer(accounts[1])[player_struct.index("playerState")] == LUNGED

def test_BRACED():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  chain.mine(1)
  game.brace({'from':accounts[1]})
  chain.mine(1)
  assert game.ownerToPlayer(accounts[1])[player_struct.index("playerState")] == BRACED

def test_reLUNGED():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  chain.mine(1)
  game.hit(accounts[0], {'from':accounts[1]})
  chain.mine(20)
  # accounts[1] is still LUNGED, but they should be able to hit again
  try:
    game.hit(accounts[2], {'from':accounts[1]})
    assert True
  except:
    assert False

def test_reBRACED():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  chain.mine(1)
  game.brace({'from':accounts[1]})
  chain.mine(6)
  # accounts[1] is still BRACED, but they should be able to brace again
  try:
    game.brace({'from':accounts[1]})
    assert True
  except:
    assert False


def test_already_playing_fail():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  try:
    game.registerPlayer(12, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  except:
    assert True


def test_max_players_fail():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  try:
    game.registerPlayer(14, 1, 1, 1, {'from': accounts[4], 'value': '10 wei'})
  except:
    assert True

def test_allowance_pass():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(1, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 17, {'from': accounts[1], 'value': '10 wei'})
  assert game.playerCount() == 2

def test_allowance_fail():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  try:
    game.registerPlayer(1, 1, 1, 18, {'from': accounts[1], 'value': '10 wei'})
  except:
    assert True

def test_cost_fail():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  try:
    game.registerPlayer(1, 1, 1, 18, {'from': accounts[1], 'value': '1 wei'})
  except:
    assert True

def test_winner():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})

  game.hit(accounts[0], {'from':accounts[1]})
  chain.mine(20);
  game.hit(accounts[2], {'from':accounts[1]})
  chain.mine(20);
  game.hit(accounts[3], {'from':accounts[1]})
  assert game.winner() == accounts[1]

def test_hit_too_fast():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  game.hit(accounts[0], {'from':accounts[1]})
  try:
    game.hit(accounts[2], {'from':accounts[1]})
  except:
    assert True


def test_winner_gets_paid():
  game = Game.deploy(20, 4, '5 wei', {'from': accounts[0]})

  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})

  start_balance = accounts[1].balance()

  game.hit(accounts[0], {'from':accounts[1]})
  chain.mine(20);
  game.hit(accounts[2], {'from':accounts[1]})
  chain.mine(20);
  game.hit(accounts[3], {'from':accounts[1]})

  stop_balance = accounts[1].balance()

  assert start_balance < stop_balance

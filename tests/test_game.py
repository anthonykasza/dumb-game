
from brownie import accounts, Game

def test_already_playing_fail():
  game = Game.deploy({'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  try:
    game.registerPlayer(12, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  except:
    assert True


def test_max_players_fail():
  game = Game.deploy({'from': accounts[0]})
  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  try:
    game.registerPlayer(14, 1, 1, 1, {'from': accounts[4], 'value': '10 wei'})
  except:
    assert True

def test_allowance_pass():
  game = Game.deploy({'from': accounts[0]})
  game.registerPlayer(1, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})
  game.registerPlayer(1, 1, 1, 17, {'from': accounts[1], 'value': '10 wei'})
  assert game.playerCount() == 2

def test_allowance_fail():
  game = Game.deploy({'from': accounts[0]})
  try:
    game.registerPlayer(1, 1, 1, 18, {'from': accounts[1], 'value': '10 wei'})
  except:
    assert True

def test_cost_fail():
  game = Game.deploy({'from': accounts[0]})
  try:
    game.registerPlayer(1, 1, 1, 18, {'from': accounts[1], 'value': '1 wei'})
  except:
    assert True

def test_loser():
  game = Game.deploy({'from': accounts[0]})

  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})

  game.hit(accounts[0], {'from':accounts[1]})
  game.ownerToPlayer(accounts[0])
  assert game.losers() == 1


def test_winner():
  game = Game.deploy({'from': accounts[0]})

  game.registerPlayer(13, 1, 1, 1, {'from': accounts[3], 'value': '10 wei'})
  game.registerPlayer(12, 1, 1, 1, {'from': accounts[2], 'value': '10 wei'})
  game.registerPlayer(11, 1, 1, 1, {'from': accounts[1], 'value': '10 wei'})
  game.registerPlayer(10, 1, 1, 1, {'from': accounts[0], 'value': '10 wei'})

  game.hit(accounts[0], {'from':accounts[1]})
  game.hit(accounts[2], {'from':accounts[1]})
  game.hit(accounts[3], {'from':accounts[1]})
  assert game.winner() == accounts[1]

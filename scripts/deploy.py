from brownie import Game, accounts

def deploy_game():
  Game.deploy(20, 4, '5 wei', {'from': accounts[0]})

def main():
  deploy_game()

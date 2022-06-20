
from brownie import accounts, Game, chain
import time
import random

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Rando():
  def __init__(self, game_addr, my_account):
    self.game = Game.at(game_addr)
    self.my_account = my_account
    self.opponents = []
    self.active_target = None
    self.hp = random.choice(range(10)) + 1
    self.de = random.choice(range(5)) + 1
    self.ag = random.choice(range(5)) + 1
    self.ak = 20 - (self.hp + self.de + self.ag)
    self.current_block = chain.height


  def register(self):
    self.game.registerPlayer(self.ak, self.de, self.ag, self.hp, {'from': self.my_account, 'value': '10 wei'})
    while True:
      if (self.game.gameState() != 1):
        time.sleep(1)
      break
    return


  def orient(self):
    self.current_block = chain.height
    player_count = self.game.playerCount()
    self.opponents = {self.game.players(i): self.game.ownerToPlayer(self.game.players(i)) for i in range(player_count) if self.game.players(i) != self.my_account.address}
    for a, o in self.opponents.items():
      if o[player_struct.index("hp")] <= 0:
        self.opponents.pop(a)


  def select_target(self):
    self.active_target = random.choice(opponents.keys())


  def hit(self):
    self.game.hit(self.active_target, {'from':self.my_account})


  def brace(self):
    self.game.brace()


  def do_action(self):
    action = random.choice(range(2))
    if action == 0:
      self.select_target()
      self.hit()

    elif action == 1:
      self.brace()

    elif action == 2:
      self.current_block = chain.height
      while(self.current_block == chain.height):
        time.sleep(2)

    else:
      pass

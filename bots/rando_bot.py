from bots.base_bot import Bot
from brownie import accounts, Game, chain
import time
import random

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Rando(Bot):
  def __init__(self, game_addr, my_account):
    super().__init__(game_addr, my_account)
    self.hp = random.choice(range(10)) + 1
    self.de = random.choice(range(5)) + 1
    self.ag = random.choice(range(5)) + 1
    self.ak = 20 - (self.hp + self.de + self.ag)


  def select_target(self):
    self.active_target = random.choice(self.opponents.keys())


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

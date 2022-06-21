from bots.base_bot import Bot
from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Cautious():
  def __init__(self, game_addr, my_account):
    super().__init__(game_addr, my_account)
    self.ak = 1
    self.de = 15
    self.ag = 1
    self.hp = 3


  def select_target(self):
    self.active_target = random.choice(opponents.keys())

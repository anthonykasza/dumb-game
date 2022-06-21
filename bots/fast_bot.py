# Fast bot has high agility and only attacks when all other players are LUNGED

import random
from bots.base_bot import Bot
from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Fast(Bot):
  def __init__(self, **kw):
    super().__init__(**kw)
    self.ak = 1
    self.de = 0
    self.ag = 10
    self.hp = 9

  def select_target(self):
    self.active_target = random.choice(opponents.keys())

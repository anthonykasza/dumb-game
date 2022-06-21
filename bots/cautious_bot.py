# A cautious bot that mostly just huddles in the corner and cries

from bots.base_bot import Bot
from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Cautious(Bot):
  def __init__(self, **kw):
    super().__init__(**kw)
    self.ak = 1
    self.de = 15
    self.ag = 1
    self.hp = 3

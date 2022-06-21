# an aggressive bot that focusses on attack others

import random
from bots.base_bot import Bot
from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Aggro(Bot):
  def __init__(self, **kw):
    super().__init__(**kw)
    self.ak = 10
    self.de = 0
    self.ag = 5
    self.hp = 5

  def select_target(self):
    weakest = None;
    for a,o in self.opponents.items():
      # if we can knock someone out right now, select them. target the weak.
      if o[player_struct.index("hp")] <= self.ak and o[player_struct.index("playerState")] != BRACED:
        self.active_target = a
        return
      if not weakest:
        weakest = a
      elif o[player_struct.index("hp")] < self.opponents[a][player_struct.index("hp")]:
        weakest = a
    if weakest:
      self.active_target = weakest
    else:
      self.active_target = random.choice(opponents.keys())

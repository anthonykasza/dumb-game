
from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Cautious():
  def __init__(self, game_addr, my_account):
    self.game = Game.at(game_addr)
    self.my_account = my_account
    self.opponents = []
    self.active_target = None
    self.ak = 1
    self.de = 15
    self.ag = 1
    self.hp = 3


  def register(self):
    self.game.registerPlayer(self.ak, self.de, self.ag, self.hp, {'from': self.my_account, 'value': '10 wei'})
    while True:
      if (self.game.gameState() != 1):
        time.sleep(1)
      # as soon as the game is playable, brace yourself
      self.brace()
      break
    return


  def orient(self):
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
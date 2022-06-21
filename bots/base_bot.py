# Base class for all Bots

from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Bot():
  def __init__(self, **kw):
    self.game_addr = kw['game_addr']
    self.my_account = kw['my_account']

    self.game = Game.at(self.game_addr)
    self.opponents = {}
    self.active_target = None
    self.current_block = chain.height
    self.ak = 0
    self.de = 0
    self.ag = 0
    self.hp = 1


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
    self.opponents = {}
    for i in range(player_count):
      player_addr = self.game.players(i)
      player = self.game.ownerToPlayer(player_addr)
      if player_addr != self.my_account.address and player[player_struct.index("hp")] > 0:
        self.opponents[self.game.players(i)] = self.game.ownerToPlayer(self.game.players(i))


  def select_target(self):
    pass


  def ready(self):
    if len(self.opponents) == 0:
      return False

    p = self.game.ownerToPlayer(self.my_account)
    p_status = p[player_struct.index("playerState")]
    p_prev_block = p[player_struct.index("prevActionBlock")]

    if p_prev_block == 0:
      return True

    if p_status == BRACED:
      # 5 is a magic number. it is the braceDuration value from the updatePlayerState function in the Game contract
      if chain.height - p_prev_block > 5:
        return True
      else:
        return False

    elif p_status == LUNGED:
      if chain.height - p_prev_block >= self.game.statsAllowance - self.ag:
        return True
      else:
        return False

    elif p_status == READY:
      return True

    else:
      return True


  def hit(self):
    if not self.ready():
      return
    self.game.hit(self.active_target, {'from':self.my_account})

  def brace(self):
    if not self.ready():
      return
    self.game.brace()

from brownie import accounts, Game, chain
import time

player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

class Bot():
  def __init__(self, **kw):
    game_addr = kw['game_addr']
    my_account = kw['my_account']

    self.game = Game.at(game_addr)
    self.my_account = my_account
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

  def hit(self):
    # TODO: add logic that ensures a bot doesn't try to hit when it's LUNGED and cannot hit
    if len(self.opponents) > 0:
      self.game.hit(self.active_target, {'from':self.my_account})

  def brace(self):
    previous_brace_block = self.game.ownerToPlayer(self.my_account)[player_struct.index("prevActionBlock")]
    # the magic number 5 is the braceDuration from the Game contract's updatePlayerState function
    # the magic number 0 is because the default value for prevActionBlock is zero
    if previous_brace_block == 0 or previous_brace_block < chain.height - 5:
      self.game.brace()

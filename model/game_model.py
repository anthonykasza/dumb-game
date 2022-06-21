import mesa
from mesa import Model, Agent
from mesa.time import RandomActivation

from brownie import accounts, Game, chain

from bots.aggro_bot import Aggro
from bots.cautious_bot import Cautious
from bots.rando_bot import Rando


player_struct = ["ak", "de", "ag", "hp", "luck", "playerState", "prevActionBlock"]
READY = 0
BRACED = 1
LUNGED = 2

statsAllowance = 20
maxPlayers = 4
gameCost = '5 wei'


class AggroAgent(Aggro, mesa.Agent):
  def __init__(self, **kw):
    super().__init__(**kw)
    self.unique_id = kw['unique_id']
    self.register()

  def step(self):
    self.orient()
    self.select_target()
    self.hit



class CautiousAgent(Cautious, mesa.Agent):
  def __init__(self, **kw):
    super().__init__(**kw)
    self.unique_id = kw['unique_id']
    self.register()

  def step(self):
    self.orient()
    self.brace()



class RandoAgent(Rando, mesa.Agent):
  def __init__(self, **kw):
    super().__init__(**kw)
    self.unique_id = kw['unique_id']
    self.register()

  def step(self):
    self.orient()
#    self.do_rand_action()




class GameModel(mesa.Model):
  def __init__(self):
    self.game = Game.deploy(statsAllowance, maxPlayers, gameCost, {'from': accounts[0]})
    self.schedule = mesa.time.RandomActivation(self)

    self.aa = AggroAgent(model=self, unique_id=0, game_addr=self.game.address, my_account=accounts[0])
    self.ca = CautiousAgent(model=self, unique_id=1, game_addr=self.game.address, my_account=accounts[1])
    self.ra1 = RandoAgent(model=self, unique_id=2, game_addr=self.game.address, my_account=accounts[2])
    self.ra2 = RandoAgent(model=self, unique_id=3, game_addr=self.game.address, my_account=accounts[3])

    self.schedule.add(self.aa)
    self.schedule.add(self.ca)
    self.schedule.add(self.ra1)
    self.schedule.add(self.ra2)


  def step(self):
    chain.mine(1)
    self.schedule.step()

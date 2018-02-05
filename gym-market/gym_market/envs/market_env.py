import gym
import csv
from gym import error, space, utils
from gym.utils import seeding

class MarketFoo(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, file_path, init_money=10000):
    self.actions = [
      "LONG",
      "SHORT",
      "NOP",
    ]
    self.action_space = spaces.Discrete(len(self.actions))

    self.input_file = open(file_path)
    self.csv_reader = csv.reader(f)
    self.header = self.csv_reader.next()

    self.state = self.csv_reader.next()
    self.next_state = nil

    self.money = init_money
    self.value = self.money
    self.bitcoin = 0.0

  def _step(self, action):
    bool terminated = False
    try:
      self.next_state = self.csv_reader.next()
      self.value = self.bitcoin * self
    except:
      terminated = True
    pass

  def _reset(self):
    pass

  def _render(self, mode='human', close=False):
    pass

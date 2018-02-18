import csv
import gym
import os

from gym import error, spaces, utils
from gym.utils import seeding

class MarketEnv(gym.Env):
  """
  A openai gym environment to simulate bitcoin market.

  Limitation:
    1) We either spend all money to buy bitcoin or sell all bitcoin for money;
    2) The current only input is a csv containing candlestick chart data (e.g. kaggle data.)
  """

  metadata = {'render.modes': ['human']}

  def __init__(self, file_name='test.csv', init_money=10000):
    self.actions = [
      "LONG",
      "SHORT",
      "NOP",
    ]
    self.action_space = spaces.Discrete(len(self.actions))

    file_path = os.path.join(os.path.dirname(__file__), file_name)
    print file_path
    self.input_file = open(file_path)
    self.csv_reader = csv.reader(self.input_file)
    self.header = self.csv_reader.next()

    self.state = map(float, self.csv_reader.next())
    print self.state
    self.next_state = None

    self.money = init_money
    self.value = self.money
    self.bitcoin = 0.0

  # TODO: Need discuss how to define reward.
  # TODO: It might be better to not include money in the environment.
  def step(self, action):
    """
    Parameters:
      action: int. The index of ["LONG", "SHORT", "NOP"]

    Returns: [observation, reward, episode_over, info]
      observation: A [open, high, low, close, volume_btc, volume_currency, weighted_price] tuple
      reward: The reward in one time step.
      terminated: True if we reach the end of the historical data. Otherwise, false.
      info: null currently. (should be set for debugging)
      
    """

    # Use close price as the price.
    if action == 0 and self.money > 0:
      self.bitcoin += self.money / self.state[4]
      self.money = 0.0
    elif action == 1 and self.bitcoin > 0:
      self.money = self.bitcoin * self.state[4]
      self.bitcoin = 0.0
    else:
      pass

    terminated = False
    new_value = self.value
    try:
      self.next_state = map(float, self.csv_reader.next())
      #new value = #bitcoin* close price
      new_value = self.bitcoin * self.next_state[4] + self.money
      self.state = list(self.next_state)
    except StopIteration:
      terminated = True
      self.next_state = []
    except:
      raise

    reward = new_value - self.value
    self.value = new_value
    
    return list(self.state), reward, terminated, {'value': self.value}

  def reset(self):
    pass

  def render(self, mode='human', close=False):
    pass


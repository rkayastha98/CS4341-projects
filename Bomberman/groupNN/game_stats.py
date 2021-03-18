import sys

sys.path.insert(0, '../bomberman')

from game import Game
from real_world import RealWorld
from events import Event
import colorama
import pygame
import math


class GameStats(Game):
    """Game class"""

    def go(self, wait=0):
        """ Main game loop. """

        # if wait is 0:
        #     def step():
        #         pygame.event.clear()
        #         input("Press Enter to continue or CTRL-C to stop...")
        # else:
        #     def step():
        #         pygame.time.wait(abs(wait))
        #
        # colorama.init(autoreset=True)
        # self.display_gui()
        # self.draw()
        # step()
        result = 0
        done = False
        while not done:
            (self.world, self.events) = self.world.next()
            # print( self.events)
            if Event.CHARACTER_FOUND_EXIT in [event.tpe for event in self.events]:
                result = 1
            # self.display_gui()
            # self.draw()
            # step()
            self.world.next_decisions()
            done = self.done()

        return result
        # colorama.deinit()

